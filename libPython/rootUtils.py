import ROOT as rt
import math
from fitUtils import *
import ctypes
import scipy.stats as stats

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
        print('Cuts:', cuts)
        print('hPass entries:', hPass[ib].GetEntries())
        print('hFail entries:', hFail[ib].GetEntries())

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
        if passI > 0:
            from ROOT import TGraphAsymmErrors
            graphP = TGraphAsymmErrors(hPass[ib])
            graphF = TGraphAsymmErrors(hFail[ib])

            graphEff = TGraphAsymmErrors()

            graphEff.Divide(graphP, graphF, "cl=0.683 mode")
            if graphEff.GetN() > 0:
                eff = graphEff.GetY()[0]
                e_eff = graphEff.GetErrorY(0)
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
import matplotlib.pyplot as plt

def getAllEffi(info, bindef):
    effis = {}
    effis_egamma = {}

    if not info['mcNominal'] is None and os.path.isfile(info['mcNominal']):
        rootfile = rt.TFile(info['mcNominal'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        bin1 = 11
        bin2 = 70
        eP = -1.
        eF = -1.
        nP = hP.IntegralAndError(bin1,bin2,ctypes.c_double(eP))
        nF = hF.IntegralAndError(bin1,bin2,ctypes.c_double(eF))


        custom_bins = TArrayD(2)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()


        hP_rebin = hP.Rebin(1, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(1, "hF_rebin", custom_bins.GetArray())

        hP_rebin.Sumw2()
        hF_rebin.Sumw2()

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        effis_egamma['mcNominal'] = computeEffi(nP,nF,eP,eF)
        efficiency_egamma = effis_egamma['mcNominal'][0]
        efficiency_error_egamma = effis_egamma['mcNominal'][0]

        if nP + nF != 0:
            efficiency_explicitly = nP / (nP + nF)
        else:
            efficiency_explicitly = 0.0

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        print("mcNominal Efficiency Divide:", efficiency)
        print("mcNominal Efficiency err Divide:", efficiency_error)
    #    print("Efficiency explicitly:", efficiency_explicitly)
    #    print("efficiency egamma:", efficiency_egamma)
    #    print("Efficiency err egamma:", efficiency_error_egamma)

    #    print("nP:", nP)
    #    print("nF:", nF)
    #    print("eP:", eP)
    #    print("eF:", eF)
    #    print("hP bin content:", hP.GetBinContent(1))
    #    print("hF bin content:", hF.GetBinContent(1))
    #    print("hP_rebin bin content:", hP_rebin.GetBinContent(1))
    #    print("hF_rebin bin content:", hF_rebin.GetBinContent(1))
    #    print("hTotal bin content:", hTotal.GetBinContent(1))
    #    print("hP bin err:", hP.GetBinError(1))
    #    print("hF bin err:", hF.GetBinError(1))
    #    print("hP_rebin bin err:", hP_rebin.GetBinError(1))
    #    print("hF_rebin bin err:", hF_rebin.GetBinError(1))
    #    print("hTotal bin err:", hTotal.GetBinError(1))

        effis['mcNominal'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['mcNominal'] = [-1, -1]


    if not info['tagSel'] is None and os.path.isfile(info['tagSel']):
        rootfile = rt.TFile(info['tagSel'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        bin1 = 11
        bin2 = 70
        eP = -1.
        eF = -1.
        nP = hP.IntegralAndError(bin1,bin2,ctypes.c_double(eP))
        nF = hF.IntegralAndError(bin1,bin2,ctypes.c_double(eF))

        custom_bins = TArrayD(2)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()

        hP_rebin = hP.Rebin(1, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(1, "hF_rebin", custom_bins.GetArray())

        hP_rebin.Sumw2()
        hF_rebin.Sumw2()

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
        #    efficiency = nP/(nP+nF)
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        print("tagSel Efficiency Divide:", efficiency)
        print("tagSel Efficiency err Divide:", efficiency_error)

        effis['tagSel'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['tagSel'] = [-1, -1]

    if not info['mcAlt'] is None and os.path.isfile(info['mcAlt']):
        rootfile = rt.TFile(info['mcAlt'], 'read')
        hP = rootfile.Get('%s_Pass' % bindef['name'])
        hF = rootfile.Get('%s_Fail' % bindef['name'])

        bin1 = 11
        bin2 = 70
        eP = -1.
        eF = -1.
        nP = hP.IntegralAndError(bin1,bin2,ctypes.c_double(eP))
        nF = hF.IntegralAndError(bin1,bin2,ctypes.c_double(eF))

        custom_bins = TArrayD(2)
        custom_bins[0] = 0
        custom_bins[1] = hP.GetXaxis().GetXmax()

        hP_rebin = hP.Rebin(1, "hP_rebin", custom_bins.GetArray())
        hF_rebin = hF.Rebin(1, "hF_rebin", custom_bins.GetArray())

        hP_rebin.Sumw2()
        hF_rebin.Sumw2()

        hTotal = hP_rebin.Clone("hTotal")
        hTotal.Add(hF_rebin)

        graph = TGraphAsymmErrors()
        graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
        #    efficiency = nP/(nP+nF)
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        print("mcAlt Efficiency Divide:", efficiency)
        print("mcAlt Efficiency err Divide:", efficiency_error)

        effis['mcAlt'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['mcAlt'] = [-1, -1]



    if not info['dataNominal'] is None and os.path.isfile(info['dataNominal']):
        rootfile = rt.TFile(info['dataNominal'], 'read')
        from ROOT import RooFit, RooFitResult, TH1D
        fitresP = rootfile.Get('%s_resP' % bindef['name'])
        fitresF = rootfile.Get('%s_resF' % bindef['name'])
        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')

        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()
#from hist
#        rootfile = rt.TFile(info['data'], 'read')
#        hP_hist = rootfile.Get('%s_Pass' % bindef['name'])
#        hF_hist = rootfile.Get('%s_Fail' % bindef['name'])
#        custom_bins = TArrayD(2)
#        custom_bins[0] = 0
#        custom_bins[1] = hP_hist.GetXaxis().GetXmax()
#        hP_rebin = hP_hist.Rebin(1, "hP_rebin", custom_bins.GetArray())
#        hF_rebin = hF_hist.Rebin(1, "hF_rebin", custom_bins.GetArray())
#        hTotal_hist = hP_rebin.Clone("hTotal_hist")
#        hTotal_hist.Add(hF_rebin)
#        error_p = hP_rebin.GetBinError(1)
#        error_f = hF_rebin.GetBinError(1)
#        error_total = hTotal_hist.GetBinError(1)
#        graph_hist = TGraphAsymmErrors()
#        graph_hist.Divide(hP_rebin, hTotal_hist, "cl=0.683 cp")

#from fit
        hP = TH1D("hP", "Pass Histogram", 1, 0, 1)
        hP.Sumw2()
        hF = TH1D("hF", "Fail Histogram", 1, 0, 1)
        hF.Sumw2()
        hTotal = TH1D("hTotal", "Total Histogram", 1, 0, 1)
        hP.SetBinContent(1, nP)
        hF.SetBinContent(1, nF)
        hP.SetBinError(1, eP)
        hF.SetBinError(1, eF)
#        hP.SetBinError(1, error_p)
#        hF.SetBinError(1, error_f)
        hTotal.SetBinContent(1, nP + nF)
        hTotal.SetBinError(1, rt.TMath.Sqrt(eP**2 + eF**2))
#        hTotal.SetBinError(1, error_total)
        graph = TGraphAsymmErrors()
        graph.Divide(hP, hTotal, "cl=0.683 b(1,1) mode")


        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1
        print("nP:", nP)
        print("nF:", nF)
        print("eP:", eP)
        print("eF:", eF)

#        print("for dataNominal from fit:")
        print("dataNominal Efficiency from fit:", efficiency)
        print("dataNominal Efficiency err from fit:", efficiency_error)
#        print("hP bin content from fit:", hP.GetBinContent(1))
#        print("hF bin content from fit:", hF.GetBinContent(1))
#        print("hTotal bin content from fit:", hTotal.GetBinContent(1))
#        print("hP bin err from fit:", hP.GetBinError(1))
#        print("hF bin err from fit:", hF.GetBinError(1))
#        print("hTotal bin err from fit:", hTotal.GetBinError(1))

#        print("for dataNominal from hist:")
#        print("efficiency from hist:", efficiency)
#        print("Efficiency err from hist:", efficiency_error)
#        print("hP bin content from hist:", hP.GetBinContent(1))
#        print("hF bin content from hist:", hF.GetBinContent(1))
#        print("hP bin err from hist:", hP.GetBinError(1))
#        print("hF bin err from hist:", hF.GetBinError(1))
#        print("hP_rebin bin content from hist:", hP_rebin.GetBinContent(1))
#        print("hF_rebin bin content from hist:", hF_rebin.GetBinContent(1))
#        print("hTotal bin content from hist:", hTotal.GetBinContent(1))
#        print("hP_rebin bin err from hist:", hP_rebin.GetBinError(1))
#        print("hF_rebin bin err from hist:", hF_rebin.GetBinError(1))
#        print("hTotal bin err from hist:", hTotal.GetBinError(1))

        effis['dataNominal'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['dataNominal'] = [-1, -1]

    if not info['dataAltSig'] is None and os.path.isfile(info['dataAltSig']):
        rootfile = rt.TFile(info['dataAltSig'], 'read')
        from ROOT import RooFit, RooFitResult,TH1D
        fitresP = rootfile.Get('%s_resP' % bindef['name'])
        fitresF = rootfile.Get('%s_resF' % bindef['name'])

        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')

        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()

        hP = TH1D("hP", "Pass Histogram", 1, 0, 1)
        hF = TH1D("hF", "Fail Histogram", 1, 0, 1)
        hTotal = TH1D("hTotal", "Total Histogram", 1, 0, 1)
        hP.SetBinContent(1, nP)
        hF.SetBinContent(1, nF)
        hP.SetBinError(1, eP)
        hF.SetBinError(1, eF)
        hTotal.SetBinContent(1, nP + nF)
        hTotal.SetBinError(1, rt.TMath.Sqrt(eP**2 + eF**2))

        graph = TGraphAsymmErrors()
    #    graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")
        graph.Divide(hP, hTotal, "cl=0.683 b(1,1) mode")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
        #    efficiency = nP/(nP+nF)
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        print("dataAltSig Efficiency from fit:", efficiency)
        print("dataAltSig Efficiency err from fit:", efficiency_error)

        effis['dataAltSig'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['dataAltSig'] = [-1, -1]


    if not info['dataAltBkg'] is None and os.path.isfile(info['dataAltBkg']):
        rootfile = rt.TFile(info['dataAltBkg'], 'read')
        from ROOT import RooFit, RooFitResult,TH1D
        fitresP = rootfile.Get('%s_resP' % bindef['name'])
        fitresF = rootfile.Get('%s_resF' % bindef['name'])

        fitP = fitresP.floatParsFinal().find('nSigP')
        fitF = fitresF.floatParsFinal().find('nSigF')

        nP = fitP.getVal()
        nF = fitF.getVal()
        eP = fitP.getError()
        eF = fitF.getError()
        rootfile.Close()

        hP = TH1D("hP", "Pass Histogram", 1, 0, 1)
        hF = TH1D("hF", "Fail Histogram", 1, 0, 1)
        hTotal = TH1D("hTotal", "Total Histogram", 1, 0, 1)
        hP.SetBinContent(1, nP)
        hF.SetBinContent(1, nF)
        hP.SetBinError(1, eP)
        hF.SetBinError(1, eF)
        hTotal.SetBinContent(1, nP + nF)
        hTotal.SetBinError(1, rt.TMath.Sqrt(eP**2 + eF**2))

        graph = TGraphAsymmErrors()
    #    graph.Divide(hP_rebin, hTotal, "cl=0.683 b(1,1) mode")
        graph.Divide(hP, hTotal, "cl=0.683 cp")

        if graph.GetN() > 0:
            efficiency = graph.GetY()[0]
        #    efficiency = nP/(nP+nF)
            efficiency_error = graph.GetErrorY(0)
        else:
            efficiency = -1
            efficiency_error = -1

        print("dataAltBkg Efficiency from fit:", efficiency)
        print("dataAltBkg Efficiency err from fit:", efficiency_error)

        effis['dataAltBkg'] = [efficiency, efficiency_error]
        rootfile.Close()
    else:
        effis['dataAltBkg'] = [-1, -1]

    return effis
