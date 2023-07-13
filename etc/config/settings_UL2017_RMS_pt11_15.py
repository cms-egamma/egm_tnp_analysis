#############################################################
########## General settings
#############################################################
# flag to be Tested
cutpass80 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.967083,0.929117,0.726311)
cutpass90 = '(( abs(probe_sc_eta) < 0.8 && probe_Ele_nonTrigMVA > %f ) ||  ( abs(probe_sc_eta) > 0.8 && abs(probe_sc_eta) < 1.479&& probe_Ele_nonTrigMVA > %f ) || ( abs(probe_sc_eta) > 1.479 && probe_Ele_nonTrigMVA > %f ) )' % (0.913286,0.805013,0.358969)

runs="BCDEF"

# flag to be Tested
flags = {
    'passingVeto'   : '(passingVeto   == 1)',
    'passingLoose'  : '(passingLoose  == 1)',
    'passingMedium' : '(passingMedium == 1)',
    'passingTight'  : '(passingTight  == 1)',
    'passingMVA80'  : cutpass80,
    'passingMVA90'  : cutpass90,
    'passingElID17UL_Ana'   : '(el_IsoMVA17UL   == 1 && fabs(el_sip) < 4 && fabs(el_dz) < 1 && fabs(el_dxy) < 0.5)',
    }
# baseOutDir = '/eos/user/a/asculac/test_altSigaltBkg_lowpt_mergedEta'
baseOutDir = '/eos/user/a/asculac/final_RMS_egm_TEST_midpt'
#############################################################
########## samples definition  - preparing the samples
#############################################################
### samples are defined in etc/inputs/tnpSampleDef.py
### not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSampleDef_17 as tnpSamples
tnpTreeDir = 'tnpEleIDs' 

samplesDef = {
    'data'   : tnpSamples.Moriond18_94X['data_Run2017{0}'.format(runs[0])].clone(),
    'mcNom'  : tnpSamples.Moriond18_94X['DY_madgraph'].clone(),
    'mcAlt'  : tnpSamples.Moriond18_94X['DY_amcatnlo'].clone(),
    'tagSel' : tnpSamples.Moriond18_94X['DY_madgraph'].clone(),
}

## can add data sample easily

for r in runs[1:]:
    samplesDef['data'].add_sample( tnpSamples.Moriond18_94X['data_Run2017{0}'.format(r)] )

## some sample-based cuts... general cuts defined here after
## require mcTruth on MC DY samples and additional cuts
## all the samples MUST have different names (i.e. sample.name must be different for all)
## if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'  ].set_cut('run >= 273726')
samplesDef['data' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_tnpTree(tnpTreeDir)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_tnpTree(tnpTreeDir)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_tnpTree(tnpTreeDir)
#if not samplesDef['mcAlt_tagSel'] is None: samplesDef['mcAlt_tagSel'].set_tnpTree(tnpTreeDir)

if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_mcTruth()
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_mcTruth()
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_mcTruth()
if not samplesDef['tagSel'] is None:
    samplesDef['tagSel'].rename('mcAltSel_DY_madgraph')
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 37') #canceled non trig MVA cut
# if not samplesDef['mcAlt_tagSel'] is None: samplesDef['mcAlt_tagSel'].set_mcTruth()
# if not samplesDef['mcAlt_tagSel'] is None:
#     samplesDef['mcAlt_tagSel'].rename('mcAlt_tag_DY_madgraph')
#     samplesDef['mcAlt_tagSel'].set_cut('tag_Ele_pt > 37') #apply tag cut on alt mc

## set MC weight, simple way (use tree weight) 
#weightName = 'totWeight'
#if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
#if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
#if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)

## set MC weight, can use several pileup rw for different data taking periods
weightName = 'weights_2017_runBCDEF.totWeight'
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_weight(weightName)
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_weight(weightName)
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_weight(weightName)
# if not samplesDef['mcAlt_tagSel'] is None: samplesDef['mcAlt_tagSel'].set_weight(weightName)
if not samplesDef['mcNom' ] is None: samplesDef['mcNom' ].set_puTree('/eos/cms/store/group/phys_egamma/swmukher/UL2017/PU_miniAOD/DY_amcatnloext_ele.pu.puTree.root')
if not samplesDef['mcAlt' ] is None: samplesDef['mcAlt' ].set_puTree('/eos/cms/store/group/phys_egamma/swmukher/UL2017/PU_miniAOD/DY_madgraph_ele.pu.puTree.root')
if not samplesDef['tagSel'] is None: samplesDef['tagSel'].set_puTree('/eos/cms/store/group/phys_egamma/swmukher/UL2017/PU_miniAOD/DY_amcatnloext_ele.pu.puTree.root')

######### 2017 ##############
#merged eta
# biningDef = [

#     { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, 2.5] },
#     { 'var' : 'el_pt' , 'type': 'float', 'bins': [7, 11, 15] },
# ]

# biningDef = [

#     { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.3, -2.0, -1.7, -1.5, -1.3, -1.0, -0.5, 0, 0.5, 1.0, 1.3, 1.5, 1.7, 2.0, 2.3, 2.5] },
#     { 'var' : 'el_pt' , 'type': 'float', 'bins': [35, 50] },
# ]

biningDef = [
    # very low pt
    # { 'var' : 'el_sc_abseta' , 'type': 'float', 'bins': [0.0, 0.5, 1.0, 1.5, 2.0, 2.5] },
    # { 'var' : 'el_pt' , 'type': 'float', 'bins': [7, 11] },
   
    # #low pt
    { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5, -2.0, -1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5, 2.0, 2.5] },
    { 'var' : 'el_pt' , 'type': 'float', 'bins': [11, 15] },
]
#############################################################
########## Cuts definition for all samples
#############################################################
### cut
cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'
addCutLowPt = 'tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45 && tag_Ele_pt > 50 '
addCutLowPtDamir = 'el_3charge==1 '

# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
additionalCuts = {}
for i in range(10):
    additionalCuts[i] = "!el_isGap"
for i in range(10):
    additionalCuts[i] = additionalCuts[i] + "&& " + addCutLowPt + " && " + addCutLowPtDamir


#############################################################
########## fitting params to tune fit by hand if necessary
#############################################################
tnpParNomFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "acmsP[60.,50.,80.]","betaP[0.05,0.01,0.08]","gammaP[0.1, -2, 2]","peakP[90.0]",
    "acmsF[60.,50.,80.]","betaF[0.05,0.01,0.08]","gammaF[0.1, -2, 2]","peakF[90.0]",
    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.1,10.0]","sosF[1,0.1,5.0]",
    "acmsP[60.,50.,10000.]","betaP[0.04,0.01,0.07]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,500.]","betaF[0.04,0.01,0.05]","gammaF[0.1, 0.005, 1]","peakF[90.5]",
    ]
#default for altsig
#   "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
#     "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,15.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.5,5.0]",
#     "acmsP[60.,50.,105.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
#     "acmsF[60.,50.,75.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]"

tnpParAltSigFit_addGaus = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,1.2,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,6.0]","alphaF[2.0,1.2,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.5,6.0]","sosF[1,0.6,5.0]",
    "meanGF[80.0,70.0,100.0]","sigmaGF[15,5.0,125.0]",
    "acmsP[60.,50.,75.]","betaP[0.04,0.01,0.06]","gammaP[0.1, 0.005, 1]","peakP[90.0]",
    "acmsF[60.,50.,85.]","betaF[0.04,0.01,0.06]","gammaF[0.1, 0.005, 1]","peakF[90.0]",
    ]
         
tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[0.9,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[0.9,0.5,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0,-0.045,0.045]",
    ]

tnpParAltSigBkgFit = [
    "meanP[-0.0,-5.0,5.0]","sigmaP[1,0.7,6.0]","alphaP[2.0,0.0,3.5]" ,'nP[3,-5,5]',"sigmaP_2[1.5,0.5,6.0]","sosP[1,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]","sigmaF[2,0.7,6.0]","alphaF[2.0,0.0,3.5]",'nF[3,-5,5]',"sigmaF_2[2.0,0.1,10.0]","sosF[1,0.1,5.0]",
    "alphaP_2[0.,-5.,5.]",
    "alphaF_2[0,-5.,5.]",
    #--above was ok for 11-15 pt

]
    
