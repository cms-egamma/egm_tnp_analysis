#!/bin/bash
echo $PWD
echo "Setting environment"

#workdir=$pwd;
#cmssw_path="$CMSSW_BASE/src";
#cd $cmssw_path; cmsenv; cd $workdir
#export PYTHONPATH=$workdir;
#make

# $1 config: etc/config/settings_pho_run2022FG.py
# $2 id
python tnpEGM_fitter.py $1 --flag $2 --checkBins
python tnpEGM_fitter.py $1 --flag $2 --createBins
python tnpEGM_fitter.py $1 --flag $2 --createHists
python tnpEGM_fitter.py $1 --flag $2 --doFit
python tnpEGM_fitter.py $1 --flag $2 --sumUp
