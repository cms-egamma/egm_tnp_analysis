Table of Contents
=================

   * [Install stable branch](#install-stable-branch)
   * [Quick description](#quick-description)
   * [The different fitting steps](#the-different-fitting-steps)
   * [The settings file](#the-settings-file)
   * [Update PU weights](#update-pu-weights)

Created by [gh-md-toc](https://github.com/ekalinin/github-markdown-toc)

# Install stable branch

```bash
cmsrel CMSSW_11_2_0
cd CMSSW_11_2_0/src
cmsenv
git clone git@github.com:cms-egamma/egm_tnp_analysis.git
cd egm_tnp_analysis
make 
```

**Note**: if you modify anything in [histUtils.pyx](libPython/histUtils.pyx) then you need to run `make cython-build` before `make` in the previous instructions.

**Note:** This package does not have any CMSSW dependenies. However, we are using this package inside the CMSSW release just to ensure that its getting appropriate version of gcc, ROOT, RooFit, etc.

# Quick description

- Package to handle analysis of tnp trees. The main tool is the python fitter `tnpEGM_fitter.py`

- The interface between the user and the fitter is solely done via the settings file `etc/config/settings.py`
  - set the flags (i.e. Working points) that can be tested
  - set the different samples and location
	- set the fitting bins
	- set the different cuts to be used
	- set the output directory

- Help message:

   ```bash
   python tnpEGM_fitter.py --help
   ```

- The settings have always to be passed to the fitter

   ```bash
   python tnpEGM_fitter.py etc/config/settings.py
   ```

- Several `settings*.py` files are setup for different eras and are located all in `etc/config/`


# The different fitting steps

Everything will be done for a specific flag (so the settings can be the same for different flags). Hence, the flag to be used must be specified each time (named myWP in following).

1. **Create the bining:** To each bin is associated a cut that can be tuned bin by bin in the `settings.py`
2. After setting up the `settings.py` check bins

   ```bash
   python tnpEGM_fitter.py etc/config/settings.py  --flag myWP --checkBins
   ```

   if  you need additinal cuts for some bins (cleaning cuts), tune cuts in the `settings.py`, then recheck.

3. Once satisfied with previous step, create the bining

   ```bash
   python tnpEGM_fitter.py etc/config/settings.py  --flag myWP --createBins
   ```

   ***CAUTION:*** when recreacting bins, the output directory is overwritten! So be sure to not redo that once you are at step2

4. **Create the histograms** with the different cuts... this is the longest step. Histograms will not be re-done later

   ```bash
   python tnpEGM_fitter.py etc/config/settings.py --flag myWP --createHists
   ```

5. **Do your first round of fits.**
   1. nominal fit

      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit
      ```

   2. MC fit to constrain alternate signal parameters [note this is the only MC fit that makes sense]

      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit --mcSig --altSig
      ```
      For some fits where we see one more peak tries to appear one can use `--addGaus` opton with altSig.
      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit --mcSig --addGaus --altSig
      ```

   3. Alternate signal fit (using constraints from previous fits)

      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit  --altSig
      ```
      If one used `--addGaus` option in previous step then in this step you have to use the `--addGaus` option.
      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit  --altSig --addGaus
      ```

   4. Alternate background fit (using constraints from previous fits)

      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit  --altBkg
      ```
   5. Alternate signal + background fit (using constraints from previous fits)

      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit  --altSigBkg
      ```
   5. **Check fits and redo failed ones.** (there is a web `index.php` in the plot directory to vizualize from the web)
      - can redo a given bin using its bin number ib. The bin number can be found from `--checkBins`, directly in the ouput dir (or web interface)

      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit --iBin ib
      ```

      the initial parameters can be tuned for this particular bin in the settings.py file. 
      
      Once the fit is good enough, do not redo all fits, just fix next failed fit.
      
   6. One can redo any kind of fit bin by bin. For instance the MC with altSig fit (if the constraint parameters were bad in the altSig for instance)

      ```bash
      python tnpEGM_fitter.py etc/config/settings.py --flag myWP --doFit --mcSig --altSig --iBin ib
      ```

6. **egm txt ouput file.** Once all fits are fine, put everything in the egm format txt file

   ```bash
   python tnpEGM_fitter.py etc/config/setting.py  --flag myWP --sumUp
   ```
   

# The settings file

The settings (for example [settings_pho_UL2017.py](etc/config/settings_pho_UL2017.py)) file includes all the necessary information for a given setup of fit

- **General settings:**
  * **flags**: this is the Working point in the tnpTree  (pass: flagCut ; fail !flagCut). The name of the flag myWP is the one to be passed to the fitter. One can handle complex flags with a cut string (root cut string):
    ```python
    flag = { 'myWP' : myWPCutString } 
    ```
  * **baseOutDir**: the output directory (will be created by the fitter)
  * **Sample definition.**
    * **tnpTreeDir**: the directory in the tnpTree (different for phoID, eleID, reco, hlt)
    * **samplesDef**: these are the main info
      - **data**: data ntuple
      - **mcNom**: nominal MC sample
      - **mcAlt**: MC for generator syst
      - **tagSel**: usually same as nominal MC + different base cuts: check the tag selection syst
    * All the samples in the **samplesDef** are defined in [tnpSampleDef.py](etc/inputs/tnpSampleDef.py).  (the attribute nEvts, lumi are not necessary for the fit per-se and can be omitted). 

- **Cuts**: 
  * **cutBase**: Define here the main cut
  * **additionalCuts**: can be used for cleaning cuts (or put additionalCuts = None)

- **Fitting parameters:** Define in this section the init parameters for the different fit, can be tuned to improve convergence.

#  Update PU weights 

1. Pileup files have to be computed with: 
   ```python
   python etc/scripts/pureweight.py
   ```
   Here one has to update the name of the directory where the files will be located and the corresponding names.

2. This python uses the following: [puReweighter.py](libPython/puReweighter.py). Here one nees to add the PU MC mix numbers that are available here: [http://cmslxr.fnal.gov/source/SimGeneral/MixingModule/python/?v=CMSSW_9_4_0](http://cmslxr.fnal.gov/source/SimGeneral/MixingModule/python/?v=CMSSW_9_4_0)

3. One also needs to update sample names here: [tnpSampleDef.py](etc/inputs/tnpSampleDef.py)

4.The data PU distrubtions can be computed using the following instructions (similar to what is done in step1):
   ```bash
   pileupCalc.py -i /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PromptReco/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt --inputLumiJSON /afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions17/13TeV/PileUp/pileup_latest.txt --calcMode true --minBiasXsec 69200 --maxPileupBin 100 --numPileupBins 100 pileup_2017_41fb.root
   ```

   Other pu files for each run, like pileup_2017_RUNB.root, pileup_2017_RUNC.root etc, can be copied from previous location. The previous location of pu directory can be found in github. For example, in this version, the location is `/eos/cms/store/group/phys_egamma/swmukher/tnp/ID_V2_2017/PU`

5. The `nvtx` and `rho` histos are not needed because we will use the pu method (type = 0) for the reweight.

**NOTE**: Before using these py in order to load the needed libraires one has to run: 
```bash
export  PYTHONPATH=$PYTHONPATH:/afs/cern.ch/user/s/soffi/scratch0/TEST/CMSSW-10-0-0-pre3/src/egm_tnp_analysis 
```
