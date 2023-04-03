import FWCore.ParameterSet.Config as cms

process = cms.Process("SKIM")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(-1))

process.source = cms.Source("PoolSource",
    fileNames=cms.untracked.vstring(
        'root://cms-xrd-global.cern.ch//store/mc/RunIISummer20UL16NanoAODAPVv9/LQToDEle_M-500_pair_bMassZero_TuneCP2_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_preVFP_v11-v1/40000/990823AF-0DA0-B141-9964-BF18C10461C7.root'
    )
)

process.electronSelection = cms.EDFilter("GenParticleSelector",
    src=cms.InputTag("prunedGenParticles"),
    cut=cms.string("abs(pdgId) == 11 && isPromptFinalState && abs(eta) < 2.5"),
    stableOnly=cms.bool(True),
)

process.skim = cms.Path(process.electronSelection)

process.out = cms.OutputModule("PoolOutputModule",
    fileName=cms.untracked.string('skim_genElectron.root'),
    outputCommands=cms.untracked.vstring("drop *",
        "keep *_prunedGenParticles_*_*",
        "keep *_slimmedGenJets_*_*",
        "keep *_slimmedMETs_*_*",
        "keep *_slimmedMuons_*_*",
        "keep *_slimmedElectrons_*_*",
        "keep *_slimmedPhotons_*_*",
        "keep *_slimmedTaus_*_*",
    ),
    SelectEvents=cms.untracked.PSet(SelectEvents=cms.vstring("skim")),
)

process.end = cms.EndPath(process.out)
