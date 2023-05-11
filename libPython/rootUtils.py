import ROOT as rt
import math
from fitUtils import *
import ctypes


def removeNegativeBins(h):
    for i in xrange(h.GetNbinsX()):
        if (h.GetBinContent(i) < 0):
            h.SetBinContent(i, 0)


def makePassFailHistograms( sample, flag, bindef, var ):
    ## open rootfile
    tree = rt.TChain(sample.tree)
    for p in sample.path:
        print ' adding rootfile: ', p
        tree.Add(p)

    if not sample.puTree is None:
        print ' - Adding weight tree: %s from file %s ' % (sample.weight.split('.')[0], sample.puTree)
        tree.AddFriend(sample.weight.split('.')[0],sample.puTree)

    ## open outputFile
    outfile = rt.TFile(sample.histFile,'recreate')
    hPass = []
    hFail = []
    for ib in range(len(bindef['bins'])):
        hPass.append(rt.TH1D('%s_Pass' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hFail.append(rt.TH1D('%s_Fail' % bindef['bins'][ib]['name'],bindef['bins'][ib]['title'],var['nbins'],var['min'],var['max']))
        hPass[ib].Sumw2()
        hFail[ib].Sumw2()

        cuts = bindef['bins'][ib]['cut']
        if sample.mcTruth :
            cuts = '%s && mcTrue==1' % cuts
        if not sample.cut is None :
            cuts = '%s && %s' % (cuts,sample.cut)

        notflag = '!(%s)' % flag
#        for aVar in bindef['bins'][ib]['vars'].keys():
#            if 'pt' in aVar or 'pT' in aVar or 'et' in aVar or 'eT' in aVar:
#                ## for high pT change the failing spectra to any probe to get statistics
#                if bindef['bins'][ib]['vars'][aVar]['min'] > 89: notflag = '( %s  || !(%s) )' % (flag,flag)

        if sample.isMC and not sample.weight is None:
            cutPass = '( %s && %s ) * %s ' % (cuts,    flag, sample.weight)
            cutFail = '( %s && %s ) * %s ' % (cuts, notflag, sample.weight)
            if sample.maxWeight < 999:
                cutPass = '( %s && %s ) * (%s < %f ? %s : 1.0 )' % (cuts,    flag, sample.weight,sample.maxWeight,sample.weight)
                cutFail = '( %s && %s ) * (%s < %f ? %s : 1.0 )' % (cuts, notflag, sample.weight,sample.maxWeight,sample.weight)
        else:
            cutPass = '( %s && %s )' % (cuts,    flag)
            cutFail = '( %s && %s )' % (cuts, notflag)

        tree.Draw('%s >> %s' % (var['name'],hPass[ib].GetName()),cutPass,'goff')
        tree.Draw('%s >> %s' % (var['name'],hFail[ib].GetName()),cutFail,'goff')


        removeNegativeBins(hPass[ib])
        removeNegativeBins(hFail[ib])

        hPass[ib].Write(hPass[ib].GetName())
        hFail[ib].Write(hFail[ib].GetName())

        bin1 = 1
        bin2 = hPass[ib].GetXaxis().GetNbins()
        epass = -1.0
        efail = -1.0
        passI = hPass[ib].IntegralAndError(bin1,bin2,ctypes.c_double(epass))
        failI = hFail[ib].IntegralAndError(bin1,bin2,ctypes.c_double(efail))
        eff   = 0
        e_eff = 0
        if passI > 0 :
            itot  = (passI+failI)
            eff   = passI / (passI+failI)
            e_eff = math.sqrt(passI*passI*efail*efail + failI*failI*epass*epass) / (itot*itot)
        print cuts
        print '    ==> pass: %.1f +/- %.1f ; fail : %.1f +/- %.1f : eff: %1.3f +/- %1.3f' % (passI,epass,failI,efail,eff,e_eff)
    outfile.Close()


def histPlotter( filename, tnpBin, plotDir ):
    print 'opening ', filename
    print '  get canvas: ' , '%s_Canv' % tnpBin['name']
    rootfile = rt.TFile(filename,"read")

    c = rootfile.Get( '%s_Canv' % tnpBin['name'] )
    c.Print( '%s/%s.png' % (plotDir,tnpBin['name']))


def computeEffi( n1,n2,e1,e2):
    effout = []
    if n1+n2 == 0 :
         eff = 0
         e_eff =0
    else:
         eff   = n1/(n1+n2)
         e_eff = 1/(n1+n2)*math.sqrt(e1*e1*n2*n2+e2*e2*n1*n1)/(n1+n2)
         if e_eff < 0.001 : e_eff = 0.001
    effout.append(eff)
    effout.append(e_eff)
    return effout


import os.path
from ROOT import TGraphAsymmErrors, TH1D, TArrayD

def getAllEffi(info, bindef):
    effis = {}

    if not info['mcNominal'] is None and os.path.isfile(info['mcNominal']):
        rootfile = rt.TFile(info['mcNominal'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        custom_bins = TArrayD(3)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()
        custom_bins[2] = hP.GetXaxis().GetXmax() + 1

        hP_rebin = hP.Rebin(2, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(2, "hF_rebin", custom_bins.GetArray())

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        effis['mcNominal'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['mcNominal'] = [-1, -1]


    if not info['tagSel'] is None and os.path.isfile(info['tagSel']):
        rootfile = rt.TFile(info['tagSel'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        custom_bins = TArrayD(3)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()
        custom_bins[2] = hP.GetXaxis().GetXmax() + 1

        hP_rebin = hP.Rebin(2, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(2, "hF_rebin", custom_bins.GetArray())

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        effis['tagSel'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['tagSel'] = [-1, -1]

    if not info['mcAlt'] is None and os.path.isfile(info['mcAlt']):
        rootfile = rt.TFile(info['mcAlt'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        custom_bins = TArrayD(3)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()
        custom_bins[2] = hP.GetXaxis().GetXmax() + 1

        hP_rebin = hP.Rebin(2, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(2, "hF_rebin", custom_bins.GetArray())

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        effis['mcAlt'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['mcAlt'] = [-1, -1]


    if not info['dataNominal'] is None and os.path.isfile(info['dataNominal']):
        rootfile = rt.TFile(info['dataNominal'], 'read')
        from ROOT import RooFit, RooFitResult
        fitresP = rootfile.Get('%s_resP' % bindef['name'])
        fitresF = rootfile.Get('%s_resF' % bindef['name'])

        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')

        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()

        rootfile = rt.TFile(info['data'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        custom_bins = TArrayD(3)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()
        custom_bins[2] = hP.GetXaxis().GetXmax() + 1

        hP_rebin = hP.Rebin(2, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(2, "hF_rebin", custom_bins.GetArray())

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        effis['dataNominal'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['dataNominal'] = [-1, -1]


    if not info['dataAltSig'] is None and os.path.isfile(info['dataAltSig']):
        rootfile = rt.TFile(info['dataAltSig'], 'read')
        from ROOT import RooFit, RooFitResult
        fitresP = rootfile.Get('%s_resP' % bindef['name'])
        fitresF = rootfile.Get('%s_resF' % bindef['name'])

        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')

        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()

        rootfile = rt.TFile(info['data'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        custom_bins = TArrayD(3)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()
        custom_bins[2] = hP.GetXaxis().GetXmax() + 1

        hP_rebin = hP.Rebin(2, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(2, "hF_rebin", custom_bins.GetArray())

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        effis['dataAltSig'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['dataAltSig'] = [-1, -1]


    if not info['dataAltBkg'] is None and os.path.isfile(info['dataAltBkg']):
        rootfile = rt.TFile(info['dataAltBkg'], 'read')
        from ROOT import RooFit, RooFitResult
        fitresP = rootfile.Get('%s_resP' % bindef['name'])
        fitresF = rootfile.Get('%s_resF' % bindef['name'])

        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')

        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()

        rootfile = rt.TFile(info['data'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        custom_bins = TArrayD(3)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()
        custom_bins[2] = hP.GetXaxis().GetXmax() + 1

        hP_rebin = hP.Rebin(2, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(2, "hF_rebin", custom_bins.GetArray())

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        effis['dataAltBkg'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['dataAltBkg'] = [-1, -1]

    return effis
