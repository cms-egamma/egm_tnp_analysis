from libPython.tnpClassUtils import tnpSample


### eos repositories
eosLegacyReReco2016 = '/eos/user/b/bng/tnpTuples/2021-02-28/2016/merged/'
eosReReco2017       = '/eos/user/b/bng/tnpTuples/2021-02-28/2017/merged/'
eosReReco2018       = '/eos/user/b/bng/tnpTuples/2021-02-28/2018/merged/'

LegacyReReco2016 = {
  'DY_madgraph'     : tnpSample('DY_madgraph',      eosLegacyReReco2016 + 'TnPTree_DY_M50_madgraphMLM.root', isMC = True, nEvts =  -1 ),
  'DY_amcatnlo'     : tnpSample('DY_amcatnlo',      eosLegacyReReco2016 + 'TnPTree_DY_M50_amcatnloFXFX.root',isMC = True, nEvts =  -1 ),
  'data_Run2016B'   : tnpSample('data_Run2016B',    eosLegacyReReco2016 + 'TnPTree_2016B.root',   lumi = 5.751),
  'data_Run2016C'   : tnpSample('data_Run2016C' ,   eosLegacyReReco2016 + 'TnPTree_2016C.root',   lumi = 2.573),
  'data_Run2016D'   : tnpSample('data_Run2016D' ,   eosLegacyReReco2016 + 'TnPTree_2016D.root',   lumi = 4.242),
  'data_Run2016E'   : tnpSample('data_Run2016E' ,   eosLegacyReReco2016 + 'TnPTree_2016E.root',   lumi = 4.025),
  'data_Run2016F'   : tnpSample('data_Run2016F' ,   eosLegacyReReco2016 + 'TnPTree_2016F.root',   lumi = 3.105),
  'data_Run2016G'   : tnpSample('data_Run2016G' ,   eosLegacyReReco2016 + 'TnPTree_2016G.root',   lumi = 7.576),
  'data_Run2016H'   : tnpSample('data_Run2016H' ,   eosLegacyReReco2016 + 'TnPTree_2016H.root',   lumi = 8.651),
}


ReReco2017 = {
  'DY_amcatnlo'   : tnpSample('DY_amcatnlo',    eosReReco2017 + 'TnPTree_DY_M50_amcatnloFXFX.root',     isMC = True, nEvts =  -1),
  'DY_madgraph'   : tnpSample('DY_madgraph',    eosReReco2017 + 'TnPTree_DY_M50_madgraphMLM.root',      isMC = True, nEvts =  -1),
  'DY_1j_madgraph': tnpSample('DY_1j_madgraph', eosReReco2017 + 'TnPTree_DY1Jets_M50_madgraphMLM.root', isMC = True, nEvts =  -1),
  'data_Run2017B' : tnpSample('data_Run2017B' , eosReReco2017 + 'TnPTree_2017RunB.root', lumi = 4.794),
  'data_Run2017C' : tnpSample('data_Run2017C' , eosReReco2017 + 'TnPTree_2017RunC.root', lumi = 9.633),
  'data_Run2017D' : tnpSample('data_Run2017D' , eosReReco2017 + 'TnPTree_2017RunD.root', lumi = 4.248),
  'data_Run2017E' : tnpSample('data_Run2017E' , eosReReco2017 + 'TnPTree_2017RunE.root', lumi = 9.315),
  'data_Run2017F' : tnpSample('data_Run2017F' , eosReReco2017 + 'TnPTree_2017RunF.root', lumi = 13.540),
}



ReReco2018 = {
  ### MiniAOD TnP for IDs scale 
  'DY_amcatnlo'   : tnpSample('DY_amcatnlo',    eosReReco2018 + 'TnPTree_DY_M50_amcatnloFXFX.root', isMC = True, nEvts =  -1),
  'DY_madgraph'   : tnpSample('DY_madgraph',    eosReReco2018 + 'TnPTree_DY_M50_madgraphMLM.root',  isMC = True, nEvts =  -1),
  'DY_powheg'     : tnpSample('DY_powheg',      eosReReco2018 + 'TnPTree_DY_M50_powheg.root',       isMC = True, nEvts =  -1),
  'data_Run2018A' : tnpSample('data_Run2018A' , eosReReco2018 + 'TnPTree_2018RunA.root', lumi = 14.028),  
  'data_Run2018B' : tnpSample('data_Run2018B' , eosReReco2018 + 'TnPTree_2018RunB.root', lumi = 7.067),
  'data_Run2018C' : tnpSample('data_Run2018C' , eosReReco2018 + 'TnPTree_2018RunC.root', lumi = 6.899),
  'data_Run2018D' : tnpSample('data_Run2018D' , eosReReco2018 + 'TnPTree_2018RunD.root', lumi = 31.748), 
}



