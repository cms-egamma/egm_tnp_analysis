from libPython.rootUtils import getAllEffi

info = {
    'data': "/eos/user/r/ryi/TagandProbe/TnP2016pre/UL2016preVFP_Run2016C_heep.root",
    'mcNominal': "/eos/user/r/ryi/TagandProbe/TnP2016pre/UL2016preVFP_DY_NLO_ptbinned_heep.root",
    'tagSel': None
}

bindef = {
    'cut': "pt>400 && pt<=650 && abs(eta)>=1.566 && abs(eta)<2.5",
    'name': "test_bin",
    'title': "test_title"
}

effis = getAllEffi(info, bindef)
print(effis)
