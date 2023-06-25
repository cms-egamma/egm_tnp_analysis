# ## samples are defined in etc/inputs/tnpSampleDef.py
# ## not: you can setup another sampleDef File in inputs
import etc.inputs.tnpSamplesUL as tnpSamples
#import etc.inputs.tnpSampleDef as tnpSamples
#############################################################
# ######### General settings
#############################################################

# flag to be Tested
flags = {
    "passingCutBasedLoose94XV2"   : "(passingCutBasedLoose94XV2  == 1)",
    "passingVeto":    "(passingVeto   == 1)",
    "passingLoose":   "(passingLoose  == 1)",
    "passingMedium":  "(passingMedium == 1)",
    "passingTight":   "(passingTight  == 1)",
#    "passingTrigger": "(passHltEle32WPTightGsf == 1) || (passHltEle115CaloIdVTGsfTrkIdTGsf == 1) || (passHltPhoton200 == 1)", #2018
#    "passingTrigger": "(passHltEle35WPTightGsf == 1) || (passHltEle115CaloIdVTGsfTrkIdTGsf == 1) || (passHltPhoton200 == 1)",  #2017
#    "passingTrigger": "(passHltEle35WPTightGsf == 1)  || (passHltPhoton200 == 1)",  #2017
    "passingTrigger": "(passHltEle27WPTightGsf == 1) ||  (passHltPhoton175 == 1)",  #2016
}
baseOutDir = "results/trigger/UL2016pre_passheep_finalresult_4etabin_moreptbin"

#############################################################
# ######### samples definition  - preparing the samples
#############################################################
tnpTreeDir = "tnpEleTrig"

#UL2018
#samplesDef = {
#    "data": tnpSamples.UL2018["data_Run2018A"].clone(),
#    "mcNom": tnpSamples.UL2018["DY_madgraph"].clone(),
##    "mcAlt": tnpSamples.UL2018["DY_amcatnloext"].clone(),
#    #"mcAlt": tnpSamples.UL2018["mc_DY_amcatnlo_ele"].clone(),
#    "mcAlt": None,
#    "tagSel": tnpSamples.UL2018["DY_madgraph"].clone(),
#}
# # can add data sample easily
#samplesDef['data'].add_sample( tnpSamples.UL2018['data_Run2018B'] )
#samplesDef['data'].add_sample( tnpSamples.UL2018['data_Run2018C'] )
#samplesDef['data'].add_sample( tnpSamples.UL2018['data_Run2018D'] )


##UL2017
#samplesDef = {
#    "data": tnpSamples.UL2017["data_Run2017B"].clone(),
#    "mcNom": tnpSamples.UL2017["DY_madgraph"].clone(),
#    "mcAlt": tnpSamples.UL2017["DY_amcatnloext"].clone(),
#    #"mcAlt": tnpSamples.UL2017["mc_DY_amcatnlo_ele"].clone(),
##    "mcAlt": None,
#    "tagSel": tnpSamples.UL2017["DY_madgraph"].clone(),
#}
# # can add data sample easily
#samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017C'] )
#samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017D'] )
#samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017E'] )
#samplesDef['data'].add_sample( tnpSamples.UL2017['data_Run2017F'] )

#UL2016_preVFP
samplesDef = {
    "data": tnpSamples.UL2016_preVFP["data_Run2016B_ver2"].clone(),
    "mcNom": tnpSamples.UL2016_preVFP["DY_amcatnloext"].clone(),
    "mcAlt": tnpSamples.UL2016_preVFP["DY_madgraph"].clone(),
#    #"mcAlt": tnpSamples.UL2016_preVFP["mc_DY_amcatnlo_ele"].clone(),
#    "mcAlt": None,
    "tagSel": tnpSamples.UL2016_preVFP["DY_amcatnloext"].clone(),
}
 # can add data sample easily
samplesDef['data'].add_sample( tnpSamples.UL2016_preVFP['data_Run2016C'] )
samplesDef['data'].add_sample( tnpSamples.UL2016_preVFP['data_Run2016D'] )
samplesDef['data'].add_sample( tnpSamples.UL2016_preVFP['data_Run2016E'] )
samplesDef['data'].add_sample( tnpSamples.UL2016_preVFP['data_Run2016F'] )

#UL2016_postVFP
#samplesDef = {
#    "data": tnpSamples.UL2016_postVFP["data_Run2016F_postVFP"].clone(),
#    "mcNom": tnpSamples.UL2016_postVFP["DY_madgraph"].clone(),
#    "mcAlt": tnpSamples.UL2016_postVFP["DY_amcatnloext"].clone(),
#    "tagSel": tnpSamples.UL2016_postVFP["DY_madgraph"].clone(),
    #"mcNom": tnpSamples.UL2016_postVFP["DY_amcatnloext"].clone(),
    #"mcAlt": tnpSamples.UL2016_postVFP["DY_madgraph"].clone(),
    #"mcAlt": None,
    #"tagSel": tnpSamples.UL2016_postVFP["DY_amcatnloext"].clone(),
#}
# can add data sample easily
#samplesDef['data'].add_sample( tnpSamples.UL2016_postVFP['data_Run2016G'] )
#samplesDef['data'].add_sample( tnpSamples.UL2016_postVFP['data_Run2016H'] )



# # some sample-based cuts... general cuts defined here after
# # require mcTruth on MC DY samples and additional cuts
# # all the samples MUST have different names (i.e. sample.name must be different for all)
# # if you need to use 2 times the same sample, then rename the second one
#samplesDef['data'].set_cut('run >= 299368')
if not samplesDef["mcNom"] is None:
    samplesDef["mcNom"].set_mcTruth()
if not samplesDef["mcAlt"] is None:
    samplesDef["mcAlt"].set_mcTruth()
if not samplesDef["tagSel"] is None:
    samplesDef["tagSel"].set_mcTruth()
if not samplesDef["tagSel"] is None:
    samplesDef["tagSel"].rename("mcAltSel_DY_madgraph_ele")
    samplesDef['tagSel'].set_cut('tag_Ele_pt > 27')  # FIXME TODO SIC: not sure about this cut value

# # set MC weight, simple way (use tree weight)
weightName = "totWeight" #Weight totWeight PUweight
if not samplesDef["mcNom"] is None:
    samplesDef["mcNom"].set_weight(weightName)
if not samplesDef["mcAlt"] is None:
    samplesDef["mcAlt"].set_weight(weightName)
if not samplesDef["tagSel"] is None:
    samplesDef["tagSel"].set_weight(weightName)

#############################################################
# ######### bining definition  [can be nD bining]
#############################################################
#biningDef = [
#    {
#        "var": "el_sc_eta",
#        "type": "float",
#        "bins": [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5],
#    },
#    {"var": "el_pt", "type": "float", "bins": [10,20,35,50,100,200,500]},
#]

biningDef = [
#   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-1.566,-1.4442, 0.0,  1.4442, 1.566,  2.5] },
 #  { 'var' : 'el_pt' , 'type': 'float', 'bins': [27, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 210, 220, 230, 240, 250, 300, 500., 1000.] },
   { 'var' : 'el_sc_eta' , 'type': 'float', 'bins': [-2.5,-2.0,-1.566,-1.4442, -0.8, 0.0, 0.8, 1.4442, 1.566, 2.0, 2.5] },
 #  { 'var' : 'el_pt' , 'type': 'float', 'bins': [35, 38, 49, 64, 82, 100, 140, 210, 400., 1000.]},
   { 'var' : 'el_pt' , 'type': 'float', 'bins': [35, 40, 50, 65, 85, 110, 140, 200, 300, 400., 1000.]},
#   { 'var' : 'el_pt' , 'type': 'float', 'bins':[27, 50, 80, 110,150,400.,1000.] },


]
#############################################################
# ######### Cuts definition for all samples
#############################################################
# ## cut
#cutBase = "tag_Ele_pt > 35 && passingHEEPV70"
#cutBase = "tag_Ele_pt > 35 && passingHEEPV70 && abs(tag_sc_eta) < 2.5"
#cutBase = "tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.5 && passingCutBasedLoose94XV2"

#cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.5 && passingCutBasedLoose94XV2' #2016
#cutBase   = 'probe_Ele_pt > 35 && passingCutBasedLoose94XV2 && abs(probe_sc_eta) < 2.5'
#cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0'
#cutBase   = 'tag_Ele_pt > 30 && abs(tag_sc_eta) < 2.1 && passingCutBasedLoose94XV2==1 && abs(el_eta) < 2.5 && el_pt > 5 && el_q*tag_Ele_q < 0' #UL2016
cutBase   = ' tag_Ele_pt > 27 && abs(tag_sc_eta) < 2.5 && el_q*tag_Ele_q < 0 && passingHEEPV70==1 && abs(el_eta) < 2.5 && el_pt > 5 ' #UL2016
#cutBase   = 'tag_Ele_pt > 35 && abs(tag_sc_eta) < 2.17 && el_q*tag_Ele_q < 0 && passingCutBasedLoose94XV2==1 && abs(el_eta) < 2.5 && el_pt > 5' #UL2017 18


# can add addtionnal cuts for some bins (first check bin number using tnpEGM --checkBins)
# additionalCuts = {
#     0: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     1: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     2: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     3: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     4: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     5: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     6: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     7: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     8: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
#     9: "tag_Ele_trigMVA > 0.92 && sqrt( 2*event_met_pfmet*tag_Ele_pt*(1-cos(event_met_pfphi-tag_Ele_phi))) < 45",
# }

# ### or remove any additional cut (default)
additionalCuts = None

#############################################################
# ######### fitting params to tune fit by hand if necessary
#############################################################
# from Jaesung
#tnpParNomFit = [
#    "meanP[-0.0,-5.0,5.0]", "sigmaP[0.5,0.1,5.0]",
#    "meanF[-0.0,-5.0,5.0]", "sigmaF[0.5,0.1,5.0]",
#    "acmsP[60.,50.,80.]", "betaP[0.05,0.01,0.08]", "gammaP[0.1, 0, 1]", "peakP[90.0]",
#    "acmsF[60.,50.,80.]", "betaF[0.05,0.01,0.08]", "gammaF[0.1, 0, 1]", "peakF[90.0]",
#    ]#original

tnpParNomFit = [
    "meanP[-0.5,0.5]", "sigmaP[0.1,0.01,1.0]",
    "meanF[-0.5,0.5]", "sigmaF[0.1,0.01,1.0]",
    "acmsP[65.,60.,70.]", "betaP[0.08,0.05,0.2]", "gammaP[0.5,0,1]", "peakP[90.0]",
    "acmsF[65.,60.,70.]", "betaF[0.08,0.05,0.2]", "gammaF[0.5,0,1]", "peakF[90.0]",
]

# for "meanP(The mean value of the Pass distribution)" and "meanF", the initial range is adjusted to [-0.5, 0.5] to limit the parameter search space.
# For "sigmaP(The standard deviation of the Pass distribution)" and "sigmaF", the step size is reduced from [0.1, 5.0] to [0.1, 1.0].
# For "acmsP(The amplitude of the Pass Crystal Ball function)" and "acmsF", the range is narrowed down to [60., 70.] to focus on specific fitting regions.
# The range for "betaP(The crystal ball transition parameter for the Pass distribution)" and "betaF" is adjusted to [0.08, 0.2] to accommodate a wider range of data distributions.
# The range for "gammaP(The crystal ball tail parameter for the Pass distribution)" and "gammaF" is set to [0.5, 1] to control the shape of the function.
#- "peakP": The peak position of the Pass distribution.

#tnpParAltSigFit = [
#    "meanP[-0.5,0.5]", "sigmaP[0.1,0.01,1.0]",  "alphaP[2.0,1.2,3.5]", 'nP[3,-5,5]', "sigmaP_2[1.5,0.5,6.0]", "sosP[1,0.5,5.0]",
#    "meanF[-0.5,0.5]", "sigmaF[0.1,0.01,1.0]", "alphaF[2.0,1.2,3.5]", 'nF[3,-5,5]', "sigmaF_2[2.0,0.5,6.0]", "sosF[1,0.5,5.0]",
#    "acmsP[65.,60.,70.]", "betaP[0.08,0.05,0.2]", "gammaP[0.5,0,1]", "peakP[90.0]",
#    "acmsF[65.,60.,70.]", "betaF[0.08,0.05,0.2]", "gammaF[0.5,0,1]", "peakF[90.0]",
#    ]

tnpParAltSigFit = [
    "meanP[-0.0,-5.0,5.0]", "sigmaP[1,0.7,6.0]",  "alphaP[2.0,1.2,3.5]", 'nP[3,-5,5]', "sigmaP_2[1.5,0.5,6.0]", "sosP[1,0.5,5.0]",
    "meanF[-0.0,-5.0,5.0]", "sigmaF[2,0.7,15.0]", "alphaF[2.0,1.2,3.5]", 'nF[3,-5,5]', "sigmaF_2[2.0,0.5,6.0]", "sosF[1,0.5,5.0]",
    "acmsP[60.,50.,75.]", "betaP[0.04,0.01,0.06]", "gammaP[0.1, 0.005, 1]", "peakP[90.0]",
    "acmsF[60.,50.,75.]", "betaF[0.04,0.01,0.06]", "gammaF[0.1, 0.005, 1]", "peakF[90.0]",
    ]#original

tnpParAltBkgFit = [
    "meanP[-0.0,-5.0,5.0]", "sigmaP[0.5,0.1,5.0]",
    "meanF[-0.0,-5.0,5.0]", "sigmaF[0.5,0.1,5.0]",
    "alphaP[0.,-5.,5.]",
    "alphaF[0.,-5.,5.]",
    ]
