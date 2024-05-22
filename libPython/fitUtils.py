import ROOT as rt
rt.gROOT.LoadMacro('./libCpp/histFitter.C+')
rt.gROOT.LoadMacro('./libCpp/RooCBExGaussShapeTNP.cc+')
rt.gROOT.LoadMacro('./libCpp/RooCMSShape.cc+')
rt.gROOT.SetBatch(1)

from ROOT import tnpFitter

import re
import math


minPtForSwitch = 70

def ptMin( tnpBin ):
    ptmin = 1
    if tnpBin['name'].find('pt_') >= 0:
        ptmin = float(tnpBin['name'].split('pt_')[1].split('p')[0])
    elif tnpBin['name'].find('et_') >= 0:
        ptmin = float(tnpBin['name'].split('et_')[1].split('p')[0])
    return ptmin

def createWorkspaceForAltSig( sample, tnpBin, tnpWorkspaceParam ):

    ### tricky: use n < 0 for high pT bin (so need to remove param and add it back)
    cbNList = ['tailLeft']
    ptmin = ptMin(tnpBin)        
    if ptmin >= 35 :
        for par in cbNList:
            for ip in range(len(tnpWorkspaceParam)):
                x=re.compile('%s.*?' % par)
                listToRM = filter(x.match, tnpWorkspaceParam)
                for ir in listToRM :
                    print '**** remove', ir
                    tnpWorkspaceParam.remove(ir)                    
            tnpWorkspaceParam.append( 'tailLeft[-1]' )

    if sample.isMC:
        return tnpWorkspaceParam

    
    fileref = sample.mcRef.altSigFit
    filemc  = rt.TFile(fileref,'read')

    from ROOT import RooFit,RooFitResult
    fitresP = filemc.Get( '%s_resP' % tnpBin['name']  )
    fitresF = filemc.Get( '%s_resF' % tnpBin['name'] )

    listOfParam = ['nF','alphaF','nP','alphaP','sigmaP','sigmaF','sigmaP_2','sigmaF_2','meanGF','sigmaGF', 'sigFracF']
    
    fitPar = fitresF.floatParsFinal()
    for ipar in range(len(fitPar)):
        pName = fitPar[ipar].GetName()
        print '%s[%2.3f]' % (pName,fitPar[ipar].getVal())
        for par in listOfParam:
            if pName == par:
                x=re.compile('%s.*?' % pName)
                listToRM = filter(x.match, tnpWorkspaceParam)
                for ir in listToRM :
                    tnpWorkspaceParam.remove(ir)                    
                tnpWorkspaceParam.append( '%s[%2.3f]' % (pName,fitPar[ipar].getVal()) )
                              
  
    fitPar = fitresP.floatParsFinal()
    for ipar in range(len(fitPar)):
        pName = fitPar[ipar].GetName()
        print '%s[%2.3f]' % (pName,fitPar[ipar].getVal())
        for par in listOfParam:
            if pName == par:
                x=re.compile('%s.*?' % pName)
                listToRM = filter(x.match, tnpWorkspaceParam)
                for ir in listToRM :
                    tnpWorkspaceParam.remove(ir)
                tnpWorkspaceParam.append( '%s[%2.3f]' % (pName,fitPar[ipar].getVal()) )

    filemc.Close()

    return tnpWorkspaceParam


#############################################################
########## nominal fitter
#############################################################
def histFitterNominal( sample, tnpBin, tnpWorkspaceParam ):
        
    tnpWorkspaceFunc = [
        "Gaussian::sigResPass(x,meanP,sigmaP)",
        "Gaussian::sigResFail(x,meanF,sigmaF)",
        "RooCMSShape::bkgPass(x, acmsP, betaP, gammaP, peakP)",
        "RooCMSShape::bkgFail(x, acmsF, betaF, gammaF, peakF)",
        ]

    tnpWorkspace = []
    tnpWorkspace.extend(tnpWorkspaceParam)
    tnpWorkspace.extend(tnpWorkspaceFunc)
    
    ## init fitter
    infile = rt.TFile( sample.histFile, "read")
    hP = infile.Get('%s_Pass' % tnpBin['name'] )
    hF = infile.Get('%s_Fail' % tnpBin['name'] )
    fitter = tnpFitter( hP, hF, tnpBin['name'] )
    infile.Close()

    ## setup
    fitter.useMinos()
    rootpath = sample.nominalFit.replace('.root', '-%s.root' % tnpBin['name'])
    rootfile = rt.TFile(rootpath,'update')
    fitter.setOutputFile( rootfile )
    
    ## generated Z LineShape
    ## for high pT change the failing spectra to any probe to get statistics
    fileTruth  = rt.TFile(sample.mcRef.histFile,'read')
    histZLineShapeP = fileTruth.Get('%s_Pass'%tnpBin['name'])
    histZLineShapeF = fileTruth.Get('%s_Fail'%tnpBin['name'])
    if ptMin( tnpBin ) > minPtForSwitch: 
        histZLineShapeF = fileTruth.Get('%s_Pass'%tnpBin['name'])
#        fitter.fixSigmaFtoSigmaP()
    fitter.setZLineShapes(histZLineShapeP,histZLineShapeF)

    fileTruth.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)
    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    fitter.fits(sample.mcTruth,sample.isMC,title)
    rootfile.Close()



#############################################################
########## alternate signal fitter
#############################################################
def histFitterAltSig( sample, tnpBin, tnpWorkspaceParam, isaddGaus=0 ):

    tnpWorkspacePar = createWorkspaceForAltSig( sample,  tnpBin, tnpWorkspaceParam )

    tnpWorkspaceFunc = [
        "tailLeft[1]",
        "RooCBExGaussShapeTNP::sigResPass(x,meanP,expr('sqrt(sigmaP*sigmaP+sosP*sosP)',{sigmaP,sosP}),alphaP,nP, expr('sqrt(sigmaP_2*sigmaP_2+sosP*sosP)',{sigmaP_2,sosP}),tailLeft)",
        "RooCBExGaussShapeTNP::sigResFail(x,meanF,expr('sqrt(sigmaF*sigmaF+sosF*sosF)',{sigmaF,sosF}),alphaF,nF, expr('sqrt(sigmaF_2*sigmaF_2+sosF*sosF)',{sigmaF_2,sosF}),tailLeft)",
        "RooCMSShape::bkgPass(x, acmsP, betaP, gammaP, peakP)",
        "RooCMSShape::bkgFail(x, acmsF, betaF, gammaF, peakF)",
        ]
    if isaddGaus==1:
        tnpWorkspaceFunc += [ "Gaussian::sigGaussFail(x,meanGF,sigmaGF)", ]
        if sample.isMC:
            tnpWorkspaceFunc += [ "sigFracF[0.5,0.0,1.0]", ]

    tnpWorkspace = []
    tnpWorkspace.extend(tnpWorkspacePar)
    tnpWorkspace.extend(tnpWorkspaceFunc)
        
    ## init fitter
    infile = rt.TFile( sample.histFile, "read")
    hP = infile.Get('%s_Pass' % tnpBin['name'] )
    hF = infile.Get('%s_Fail' % tnpBin['name'] )
    ## for high pT change the failing spectra to passing probe to get statistics 
    ## MC only: this is to get MC parameters in data fit!
    if sample.isMC and ptMin( tnpBin ) > minPtForSwitch:     
        hF = infile.Get('%s_Pass' % tnpBin['name'] )
    fitter = tnpFitter( hP, hF, tnpBin['name'] )
#    fitter.fixSigmaFtoSigmaP()
    infile.Close()

    ## setup
    rootpath = sample.altSigFit.replace('.root', '-%s.root' % tnpBin['name'])
    rootfile = rt.TFile(rootpath,'update')
    fitter.setOutputFile( rootfile )
    
    ## generated Z LineShape
    fileTruth = rt.TFile('etc/inputs/ZeeGenLevel.root','read')
    histZLineShape = fileTruth.Get('Mass')
    fitter.setZLineShapes(histZLineShape,histZLineShape)
    fileTruth.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)
    fitter.setWorkspace( workspace, isaddGaus )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    fitter.fits(sample.mcTruth,sample.isMC,title, isaddGaus)

    rootfile.Close()



#############################################################
########## alternate background fitter
#############################################################
def histFitterAltBkg( sample, tnpBin, tnpWorkspaceParam ):

    tnpWorkspaceFunc = [
        "Gaussian::sigResPass(x,meanP,sigmaP)",
        "Gaussian::sigResFail(x,meanF,sigmaF)",
        "Exponential::bkgPass(x, alphaP)",
        "Exponential::bkgFail(x, alphaF)",
        ]

    tnpWorkspace = []
    tnpWorkspace.extend(tnpWorkspaceParam)
    tnpWorkspace.extend(tnpWorkspaceFunc)
            
    ## init fitter
    infile = rt.TFile(sample.histFile,'read')
    hP = infile.Get('%s_Pass' % tnpBin['name'] )
    hF = infile.Get('%s_Fail' % tnpBin['name'] )
    fitter = tnpFitter( hP, hF, tnpBin['name'] )
    infile.Close()

    ## setup
    rootpath = sample.altBkgFit.replace('.root', '-%s.root' % tnpBin['name'])
    rootfile = rt.TFile(rootpath,'update')
    fitter.setOutputFile( rootfile )
#    fitter.setFitRange(65,115)

    ## generated Z LineShape
    ## for high pT change the failing spectra to any probe to get statistics
    fileTruth = rt.TFile(sample.mcRef.histFile,'read')
    histZLineShapeP = fileTruth.Get('%s_Pass'%tnpBin['name'])
    histZLineShapeF = fileTruth.Get('%s_Fail'%tnpBin['name'])
    if ptMin( tnpBin ) > minPtForSwitch: 
        histZLineShapeF = fileTruth.Get('%s_Pass'%tnpBin['name'])
#        fitter.fixSigmaFtoSigmaP()
    fitter.setZLineShapes(histZLineShapeP,histZLineShapeF)
    fileTruth.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)
    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    fitter.fits(sample.mcTruth,sample.isMC,title)
    rootfile.Close()


#############################################################
########## alternate signal+background fitter
#############################################################
def histFitterAltSigBkg( sample, tnpBin, tnpWorkspaceParam):

    tnpWorkspaceFunc = [
        "tailLeft[1]",
        "RooCBExGaussShapeTNP::sigResPass(x,meanP,expr('sqrt(sigmaP*sigmaP+sosP*sosP)',{sigmaP,sosP}),alphaP,nP, expr('sqrt(sigmaP_2*sigmaP_2+sosP*sosP)',{sigmaP_2,sosP}),tailLeft)",
        "RooCBExGaussShapeTNP::sigResFail(x,meanF,expr('sqrt(sigmaF*sigmaF+sosF*sosF)',{sigmaF,sosF}),alphaF,nF, expr('sqrt(sigmaF_2*sigmaF_2+sosF*sosF)',{sigmaF_2,sosF}),tailLeft)",
        "Exponential::bkgPass(x, alphaP_2)",
        "Exponential::bkgFail(x, alphaF_2)",
        ]

    tnpWorkspace = []
    tnpWorkspace.extend(tnpWorkspaceParam)
    tnpWorkspace.extend(tnpWorkspaceFunc)
            
    ## init fitter
    infile = rt.TFile(sample.histFile,'read')
    hP = infile.Get('%s_Pass' % tnpBin['name'] )
    hF = infile.Get('%s_Fail' % tnpBin['name'] )
    fitter = tnpFitter( hP, hF, tnpBin['name'] )
    infile.Close()
    
    ## setup
    rootpath = sample.altSigBkgFit.replace('.root', '-%s.root' % tnpBin['name'])
    rootfile = rt.TFile(rootpath,'update')
    fitter.setOutputFile( rootfile )
#    fitter.setFitRange(65,115)


    ## generated Z LineShape
    ## for high pT change the failing spectra to any probe to get statistics
    fileTruth = rt.TFile(sample.mcRef.histFile,'read')
    histZLineShapeP = fileTruth.Get('%s_Pass'%tnpBin['name'])
    histZLineShapeF = fileTruth.Get('%s_Fail'%tnpBin['name'])
    if ptMin( tnpBin ) > minPtForSwitch: 
        histZLineShapeF = fileTruth.Get('%s_Pass'%tnpBin['name'])
#        fitter.fixSigmaFtoSigmaP()
    fitter.setZLineShapes(histZLineShapeP,histZLineShapeF)
    fileTruth.Close()

    ### set workspace
    workspace = rt.vector("string")()
    for iw in tnpWorkspace:
        workspace.push_back(iw)
    fitter.setWorkspace( workspace )

    title = tnpBin['title'].replace(';',' - ')
    title = title.replace('probe_sc_eta','#eta_{SC}')
    title = title.replace('probe_Ele_pt','p_{T}')
    fitter.fits(sample.mcTruth,sample.isMC,title)
    rootfile.Close()


