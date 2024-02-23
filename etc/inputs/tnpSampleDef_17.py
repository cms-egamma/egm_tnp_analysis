from libPython.tnpClassUtils import tnpSample

### qll stat
summer19 = '/data_CMS/cms/asculac/TnP_tuples/UL2017/data/Summer19/'

Moriond18_94X = {
    ### MiniAOD TnP for IDs scale factors
    'DY_madgraph'              : tnpSample('DY_madgraph',
                                      # '/data_CMS/cms/asculac/TnP_tuples/UL2017/mc/Summer19/DY_19UL17_madgraph.root',
                                     '/data_CMS/cms/asculac/TnP_tuples/UL2017/mc/Summer20/DYJetsToLL_magraph_20UL17.root',
                                       isMC = True, nEvts =  -1 ),
    'DY_amcatnlo'                 : tnpSample('DY_amcatnlo',
                                       '/data_CMS/cms/asculac/TnP_tuples/UL2017/mc/Summer20/DY_amcatnlo_miniADOv2_20UL17.root', ##UPDATED TO SUMMER20
                                       isMC = True, nEvts =  -1 ),



    'data_Run2017B' : tnpSample('data_Run2017B' , summer19 + 'data_RunB_2017.root' , lumi = 4.793961427),
    'data_Run2017C' : tnpSample('data_Run2017C' , summer19 + 'data_RunC_2017.root' , lumi = 9.631214821 ),
    'data_Run2017D' : tnpSample('data_Run2017D' , summer19 + 'data_RunD_2017.root' , lumi = 4.247682053 ),
    'data_Run2017E' : tnpSample('data_Run2017E' , summer19 + 'data_RunE_2017.root' , lumi = 9.313642402 ),
    'data_Run2017F' : tnpSample('data_Run2017F' , summer19 + 'data_RunF_2017.root' , lumi = 13.510934811),

    }
