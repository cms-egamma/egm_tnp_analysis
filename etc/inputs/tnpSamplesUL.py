from libPython.tnpClassUtils import tnpSample

# eos repositories
eosUL2017 = (
    "/eos/user/r/ryi/TagandProbe/TnP2017/"
)
eosUL2018 = (
    "/eos/user/r/ryi/TagandProbe/TnP2018/"
)
eosUL2016_preVFP = (
    "/eos/user/r/ryi/TagandProbe/TnP2016pre/"
)
eosUL2016_postVFP = (
    "/eos/user/r/ryi/TagandProbe/TnP2016post/"
)

UL2017 = {
    # ## MiniAOD TnP for IDs scale factors
    "DY_madgraph": tnpSample(
        #"DY_madgraph", eosUL2017 + "DYJetsToEE.root ", isMC=True, nEvts=-1
        "DY_madgraph", eosUL2017 + "UL2017_withHEEP_LO.root", isMC=True, nEvts=-1
    ),
#    "DY_madgraphext": tnpSample(
#        #"DY_madgraph", eosUL2017 + "DYJetsToEE.root ", isMC=True, nEvts=-1
#        "DY_madgraphext", eosUL2017 + "DY_LO_ext.root", isMC=True, nEvts=-1
#    ),
    "DY_amcatnloext": tnpSample("DY_amcatnloext", eosUL2017 + "UL2017_DY_NLO_ptbinned_heep.root", isMC=True, nEvts =-1),
#    "DY_amcatnloext": tnpSample(
#        "DY_amcatnloext",
#        eosUL2017 + "DYJetsToLL_amcatnloFXFX.root",
#        isMC=True,
#        nEvts=-1,
#    ),
    "data_Run2017B": tnpSample(
        "data_Run2017B", eosUL2017 + "UL2017_Run2017B_heep.root", lumi=4.793961427
    ),
    "data_Run2017C": tnpSample(
        "data_Run2017C", eosUL2017 + "UL2017_Run2017C_heep.root", lumi=9.631214821
    ),
    "data_Run2017D": tnpSample(
        "data_Run2017D", eosUL2017 + "UL2017_Run2017D_heep.root", lumi=4.247682053
    ),
    "data_Run2017E": tnpSample(
        "data_Run2017E", eosUL2017 + "UL2017_Run2017E_heep.root", lumi=9.313642402
    ),
    "data_Run2017F": tnpSample(
        "data_Run2017F", eosUL2017 + "UL2017_Run2017F_heep.root", lumi=13.510934811
    ),
}

UL2018 = {
    # ## MiniAOD TnP for IDs scale factors
    "DY_madgraph": tnpSample(
        #"DY_madgraph", "/afs/cern.ch/user/s/scooper/work/private/cmssw/10_6_13/LegacyTriggerScaleFactors/src/EgammaAnalysis/TnPTreeProducer/python/TnPTree_mc.root", isMC=True, nEvts=-1
        "DY_madgraph", eosUL2018 + "UL2018_withHEEP_LO.root", isMC=True, nEvts=-1
    ),
    "DY_amcatnloext": tnpSample(
        "DY_amcatnloext",
        #eosUL2018 + "DYJetsToLL_amcatnloFXFX.root",
    #    eosUL2018 + "UL2018_DY_NLO_ptbinned_heep.root",
        eosUL2018 + "DY_NLO.root",
        isMC=True,
        nEvts=-1,
    ),
#    "data_Run2018A": tnpSample(
#        "data_Run2018A", "/afs/cern.ch/user/s/scooper/work/private/cmssw/10_6_13/LegacyTriggerScaleFactors/src/EgammaAnalysis/TnPTreeProducer/python/TnPTree_data.root", lumi=14.02672485
#    ),
#    "data_Run2018B": tnpSample(
#        "data_Run2018B", eosUL2018 + "EGamma_RunB.root", lumi=7.060617355
#    ),
#    "data_Run2018C": tnpSample(
#        "data_Run2018C", eosUL2018 + "EGamma_RunC.root", lumi=6.894770971
#    ),
#    "data_Run2018D": tnpSample(
#        "data_Run2018D", eosUL2018 + "EGamma_RunD.root", lumi=31.74220577
#    ),
#}
    "data_Run2018A": tnpSample(
        "data_Run2018A", eosUL2018 + "UL2018_Run2018A_heep.root", lumi=14.02672485
    ),
    "data_Run2018B": tnpSample(
        "data_Run2018B", eosUL2018 + "UL2018_Run2018B_heep.root", lumi=7.060617355
    ),
    "data_Run2018C": tnpSample(
        "data_Run2018C", eosUL2018 + "UL2018_Run2018C_heep.root", lumi=6.894770971
    ),
    "data_Run2018D": tnpSample(
        "data_Run2018D", eosUL2018 + "UL2018_Run2018D_heep.root", lumi=31.74220577
    ),
}

UL2016_preVFP = {
    # MiniAOD TnP for IDs scale factors
    "DY_madgraph": tnpSample(
        "DY_madgraph",
        eosUL2016_preVFP
        + "UL2016pre_LO_heep.root",
        isMC=True,
        nEvts=-1,
    ),
#    "DY_amcatnloext": tnpSample(
#        "DY_amcatnloext",
#        eosUL2016_preVFP
#        + "DY_NLO.root",
#        isMC=True,
#        nEvts=-1,
#    ),
    #pt-binned
    "DY_amcatnloext": tnpSample(
        "DY_amcatnloext",
        eosUL2016_preVFP
        + "UL2016preVFP_DY_NLO_ptbinned_heep.root",
        isMC=True,
        nEvts=-1,
    ),
#    "data_Run2016B": tnpSample(
#        "data_Run2016B", eosUL2016 + "UL2016_SingleEle_Run2016B.root", lumi=0.030493962
#    ),
    "data_Run2016B_ver2": tnpSample(
        "data_Run2016B_ver2",
        eosUL2016_preVFP + "UL2016preVFP_Run2016B_ver2_heep.root",
        lumi=5.879330594,
    ),
    "data_Run2016C": tnpSample(
        "data_Run2016C", eosUL2016_preVFP + "UL2016preVFP_Run2016C_heep.root", lumi=2.64992914
    ),
    "data_Run2016D": tnpSample(
        "data_Run2016D", eosUL2016_preVFP + "UL2016preVFP_Run2016D_heep.root", lumi=4.292865604
    ),
    "data_Run2016E": tnpSample(
        "data_Run2016E", eosUL2016_preVFP + "UL2016preVFP_Run2016E_heep.root", lumi=4.185165152
    ),
    "data_Run2016F": tnpSample(
        "data_Run2016F", eosUL2016_preVFP + "UL2016preVFP_Run2016F_heep.root", lumi=2.725508364
    ),
}

UL2016_postVFP = {
    # MiniAOD TnP for IDs scale factors
    "DY_madgraph": tnpSample(
        "DY_madgraph",
        eosUL2016_postVFP
        + "UL2016post_LO_heep.root",
        isMC=True,
        nEvts=-1,
    ),
#    "DY_amcatnloext": tnpSample(
#        "DY_amcatnloext",
#        eosUL2016_postVFP
#        + "DY_NLO.root",
#        isMC=True,
#        nEvts=-1,
#    ),
    #pt-binned
    "DY_amcatnloext": tnpSample(
        "DY_amcatnloext",
        eosUL2016_postVFP
        + "UL2016postVFP_DY_NLO_ptbinned_heep.root",
        isMC=True,
        nEvts=-1,
    ),

#    "DY_amcatnloext_inclusive": tnpSample(
#        "DY_amcatnloext_inclusive",
#        eosUL2016_postVFP
#        + "2016post-NLO_amc_allrange_new.root",
#        isMC=True,
#        nEvts=-1,
#    ),
    "data_Run2016F_postVFP": tnpSample(
        "data_Run2016F_postVFP",
        eosUL2016_postVFP + "UL2016postVFP_Run2016F_postVFP_heep.root",
        lumi=0.414987426,
    ),
    "data_Run2016G": tnpSample(
        "data_Run2016G", eosUL2016_postVFP + "UL2016postVFP_Run2016G_heep.root", lumi=7.634508755
    ),
    "data_Run2016H": tnpSample(
        "data_Run2016H", eosUL2016_postVFP + "UL2016postVFP_Run2016H_heep.root", lumi=8.802242522
    ),
}
