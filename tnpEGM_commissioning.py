import os,sys,copy
#import numpy as np
from root_numpy import  tree2array, array2tree

sys.path.append("..")
import etc.inputs.tnpSampleDef as tnpSamples
import libPython.tnpClassUtils as tnpClasses
import libPython.CMS_lumi as CMS_lumi
import libPython.tdrstyle as tdrstyle

import ROOT as rt
from ROOT import gStyle
from ROOT import gROOT



#################################################################################################
########## settings
#################################################################################################
treename = 'tnpEleIDs/fitter_tree'


tdrstyle.setTDRStyle()
CMS_lumi.extraText = "Preliminary"
CMS_lumi.lumi_sqrtS = "35.9 fb^{-1} (13 TeV)"

iPos = 11
iPeriod = 0


##### define data samples
dataSamples = {
#    'runBCD'  :  tnpSamples.Moriond17_80X['data_Run2016B'].clone(),
    'runH'  :  tnpSamples.Legacy2016_v1_80X['data_Run2016H'].clone(),
}
#dataSamples['runBCD'].add_sample(tnpSamples.Moriond17_80X['data_Run2016C'])
#dataSamples['runBCD'].add_sample(tnpSamples.Moriond17_80X['data_Run2016D'])

##### define mc samples
mcSamples = {
#    'runBCD'  : tnpSamples.Remini17_80X['DY_madgraph'  ].clone(),
    'runH'  : tnpSamples.Legacy2016_v1_80X['DY_madgraph_Winter17' ].clone(),
}
#mcSamples['runBCD'].set_puTree('root://eoscms.cern.ch//eos/cms/store/group/phys_egamma/tnp/80X/pu/DY_madgraph_MCWinter17_rec_rec.pu.puTree.root')
#mcSamples['runBCD'].set_weight('weights_2016_runBCD.totWeight')
weightName = 'totWeight'
#mcSamples['runBCD'].set_weight(weightName)
mcSamples['runH'].set_weight(weightName)



#### the different epochs to run over
epochs = [ 'runH' ]

### the output directory
outputdir = 'plots/commissioning/'


### the list of variables to plot (cuts are defined in the loopTree function)
cutEB = 'EB'
cutEE = 'EE'
varList = [
    tnpClasses.tnpVar('event_nPV', title = "# PV",  xmin = -0.5, xmax = 50.5, nbins = 51,),
    tnpClasses.tnpVar('rho'      , title = "#rho", nbins = 50, xmin = -0.5, xmax = 50.5),
    tnpClasses.tnpVar('el_sc_eta', title = 'SC #eta',nbins=100,xmin = -2.5,xmax = 2.5),
    tnpClasses.tnpVar('pair_mass', title = 'EB - M_{ee} [GeV]', nbins=120,xmin=60, xmax=120, cut = cutEB ),
    tnpClasses.tnpVar('pair_mass', title = 'EE - M_{ee} [GeV]', nbins=120,xmin=60, xmax=120, cut = cutEE ),
    tnpClasses.tnpVar('el_et'    , title = 'EB - E_{T} [GeV]',nbins=100,xmin=0, xmax=100, cut = cutEB),
    tnpClasses.tnpVar('el_et'    , title = 'EE - E_{T} [GeV]',nbins=100,xmin=0, xmax=100, cut = cutEE),
    tnpClasses.tnpVar('el_chIso' , title = 'EB - Charged Hadron Isolation [GeV]',nbins=100,xmin=0, xmax=5, cut = cutEB),
    tnpClasses.tnpVar('el_chIso' , title = 'EE - Charged Hadron Isolation [GeV]',nbins=100,xmin=0, xmax=5, cut = cutEE),
    tnpClasses.tnpVar('el_neuIso', title = 'EB - Neutral Hadron Isolation [GeV]',nbins=100,xmin=0, xmax=5, cut = cutEB),
    tnpClasses.tnpVar('el_neuIso', title = 'EE - Neutral Hadron Isolation [GeV]',nbins=100,xmin=0, xmax=5, cut = cutEE),
    tnpClasses.tnpVar('el_phoIso', title = 'EB - photon Isolation [GeV]',nbins=100,xmin=0, xmax=5, cut = cutEB),
    tnpClasses.tnpVar('el_phoIso', title = 'EE - photon Isolation [GeV]',nbins=100,xmin=0, xmax=5, cut = cutEE),
    tnpClasses.tnpVar('el_sieie' , title = 'EB - #sigma_{i#etai#eta}', nbins=100,xmin=0.005,xmax=0.015, cut = cutEB),
    tnpClasses.tnpVar('el_sieie' , title = 'EE - #sigma_{i#etai#eta}', nbins=100,xmin=0.015,xmax=0.035, cut = cutEE),
    tnpClasses.tnpVar('el_dEtaIn', title = 'EB - #delta#eta_{in}', nbins=50,xmin=-0.04,xmax=0.04, cut = cutEB),
    tnpClasses.tnpVar('el_dEtaIn', title = 'EE - #delta#eta_{in}', nbins=50,xmin=-0.04,xmax=0.04, cut = cutEE),
    tnpClasses.tnpVar('el_dPhiIn', title = 'EB - #delta#phi_{in}', nbins=50,xmin=-0.2,xmax=0.2, cut = cutEB),
    tnpClasses.tnpVar('el_dPhiIn', title = 'EE - #delta#phi_{in}', nbins=50,xmin=-0.2,xmax=0.2, cut = cutEE),

#el_neuIso
#el_phoIso
    ]





#################################################################################################
########## loop over events and fill histograms
#################################################################################################
def loopTree(sample, isMC):


    tree = rt.TChain(treename)
    for p in sample.path:
        print ' adding rootfile: ', p
        tree.Add(p)

    friendTreeName=''
    if not sample.puTree is None:
        print ' - Adding weight tree: %s from file %s ' % (sample.weight.split('.')[0], sample.puTree)
        friendTreeName = sample.weight.split('.')[0]
        tree.AddFriend(sample.weight.split('.')[0],sample.puTree)

    print "friendTreeName is ", friendTreeName


    if(isMC):
        friendTree = tree.GetFriend(friendTreeName)

    treeVars = ['tag_Ele_pt','tag_sc_abseta','passingLoose80X','el_pt','el_sc_abseta',
                'el_neuIso','el_phoIso','el_chIso',
                'tag_Ele_q','el_q']
    histList = []
    for var in varList:
        if not var.varName() in treeVars: treeVars.append(var.varName())
        histList.append( copy.deepcopy(var) )

    if isMC: treeVars.append('totWeight')

    print 'Getting vars: '
    print treeVars
#    tree.Print('toponly')
    events = tree2array( tree, branches = treeVars )

    nentries = 100000
    nentries = len(events)
    print 'Nentries: ', nentries
    for ev in range(nentries):
        if ev % 100000 == 0 : print ' Nevts: ', ev

        # combinedProbeIso   = (el_neuIso+el_phoIso+el_chIso)/el_pt

#        print "tag pt : mass : combinedIso ", tag_Ele_pt, " ",pair_mass, " ", combinedTagIso
        evt = events[ev]
        if evt['tag_Ele_pt'] < 35 : continue
        if evt['el_pt']      < 20 : continue
        if evt['el_q'] * evt['tag_Ele_q'] > 0 : continue
        if evt['el_sc_eta']>-1.566 and evt['el_sc_eta']<-1.4442: continue
        if evt['el_sc_eta']<1.566 and evt['el_sc_eta']>1.4442: continue
       # if int(evt['passingLoose80X']) == 0 : continue

        weight = 1
        if isMC : weight = evt['totWeight']
        for hist in histList:
            if   hist.cut is None:
                hist.get_hist().Fill( evt[hist.var], weight )
            elif hist.cut == 'EB' and evt['el_sc_abseta'] < 1.479 :
                hist.get_hist().Fill( evt[hist.var], weight )
            elif hist.cut == 'EE' and evt['el_sc_abseta'] > 1.479 :
                hist.get_hist().Fill( evt[hist.var], weight )

    return histList

######For drawing purpose
def setCanvas():

    W = 800
    H = 600
    H_ref = 600
    W_ref = 800
    T = 0.08*H_ref
    B = 0.12*H_ref
    L = 0.12*W_ref
    R = 0.04*W_ref

    c = rt.TCanvas('c','c',50,50,W,H)
    c.SetLeftMargin( L/W )
    c.SetRightMargin( R/W )
    c.SetTopMargin( T/H )
    c.SetBottomMargin( B/H )



    pad1 = rt.TPad("pad1", "The pad 80% of the height",0.0,0.2,1.0,1.0,21)
    pad2 = rt.TPad("pad2", "The pad 20% of the height",0.0,0.001,1.0,0.25,22)

    pad1.SetFillColor(0)
    pad2.SetFillColor(0)

    pad2.SetTopMargin(0.02619172);
    pad2.SetBottomMargin(0.3102846);

    pad1.Draw()
    pad2.Draw()

    return c,pad1,pad2


def setLegend():
    leg = rt.TLegend(0.72,0.75,0.9194975,0.9154704)
    leg.SetBorderSize(0)
    leg.SetTextFont(62)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(1001)

    return leg


def getRatioPlot(histData,histMC ):
    hratio = histData.Clone()

    hratio.Divide(histData,histMC)
    hratio.GetXaxis().SetTitle(histData.GetXaxis().GetTitle())

    hratio.GetXaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetTitleSize(0.09)

    hratio.GetXaxis().SetLabelFont(42)
    hratio.GetXaxis().SetLabelSize(0.11)
    hratio.GetXaxis().SetTitleSize(0.035)
    hratio.GetXaxis().SetTitleFont(62)
    hratio.GetYaxis().SetTitle("#frac{Data}{MC}")
    hratio.GetYaxis().SetLabelFont(62)
    hratio.GetYaxis().SetLabelSize(0.11)
    hratio.GetYaxis().SetTitleSize(0.13)
    hratio.GetYaxis().SetTitleOffset(0.3)

    hratio.GetYaxis().SetNdivisions(205)
    hratio.GetXaxis().SetTitleSize(0.08)
    hratio.GetXaxis().SetLabelSize(0.13)
    hratio.GetXaxis().SetTitleSize(0.13)
    hratio.GetYaxis().SetLabelSize(0.12)
    hratio.GetYaxis().SetTitleSize(0.13)
    hratio.GetYaxis().SetTitleFont(62)
    hratio.GetZaxis().SetLabelFont(62)
    hratio.GetZaxis().SetLabelSize(0.035)
    hratio.GetZaxis().SetTitleSize(0.035)
    hratio.GetZaxis().SetTitleFont(62)

    hratio.GetYaxis().SetTitleOffset(0.3)
    hratio.GetYaxis().SetTitle("#frac{Data}{MC}")

    hratio.SetMaximum(1.5)
    hratio.SetMinimum(0.5)

    return hratio




#################################################################################################
########## main
#################################################################################################
for epoch in  epochs:

    histListData = loopTree(dataSamples[epoch],0)
    histListMC   = loopTree(mcSamples[epoch]  ,1)


    os.system("mkdir -p "+ outputdir + '/' + epoch + '/linear/' )
    os.system("mkdir -p "+ outputdir + '/' + epoch + '/log/' )
    fileoutMC   = rt.TFile( outputdir + "/histoMC_%s.root"   %(epoch), "RECREATE")
    fileoutData = rt.TFile( outputdir + "/histoData_%s.root" %(epoch), "RECREATE")


    for ih in range(len(histListMC)):
        histMC   = histListMC[ih].get_hist()
        histData = histListData[ih].get_hist()
        ####save the hists first in a root file which can be used later###
        fileoutMC.cd()
        histMC.Write()

        fileoutData.cd()
        histData.Write()

        #####linear plots
        c,pad1,pad2 = setCanvas()


        histMC.SetFillColor(rt.kOrange-2)
        histMC.SetLineColor(rt.kOrange-2)

        histData.SetLineWidth(2)
        histData.SetMarkerStyle(20)
        histData.SetLineColor(1)

        print "Data integral ",histData.Integral()
        print "MC integral ",histMC.Integral()
        if not (histMC.Integral() == 0):
            scale = histData.Integral()/histMC.Integral()

        if(histMC.Integral() == 0):
           print "hist: ",histMC.GetName(), " MC integral is 0 so not plotting"
           continue

        histMC.Scale(scale)

        pad1.cd()
        gStyle.SetOptStat(0)
        histMC.GetXaxis().SetLabelSize(0)
        histMC.GetXaxis().SetTitleSize(0)
        histMC.SetMinimum(0)
        histMC.GetYaxis().SetTitle('Events')
        histMC.DrawCopy('hist')
        histData.DrawCopy('same e')
        c.Update()

        #iPeriod = 2
        #iPos = 11
        CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)

        leg = setLegend()
        leg.AddEntry(histData,"Data","P")
        leg.AddEntry(histMC, "Z#rightarrow ee (MC)","f")
        leg.Draw()
        pad1.Update()

        tex = rt.TLatex(0.4,0.85,"Z#rightarrow ee")
        tex.SetNDC()
        tex.SetLineWidth(2)
#        tex.Draw()

        pad2.cd()
        hratio = getRatioPlot(histData,histMC)
        hratio.SetTitle('')
        hratio.DrawCopy("E1")

        xlow  = histData.GetXaxis().GetXmin()
        xhigh = histData.GetXaxis().GetXmax()

        l = rt.TLine(xlow,1.,xhigh,1.)
        l.SetLineColor(2)
        l.SetLineStyle(2)
        l.SetLineWidth(2)
        l.Draw("sames")
        c.Update()

        pngname = "%s.png" % (histData.GetTitle())
        print("png name is ",pngname)
        c.Print( outputdir + '/' + epoch + '/linear/' + pngname )

        ######log plots
        c,pad1,pad2 = setCanvas()
        pad1.cd()
        pad1.SetLogy()
        histMC.SetMinimum(0.1)
        histData.SetMinimum(0.1)
        histMC.DrawCopy('hist')
        histData.DrawCopy('same e')
        CMS_lumi.CMS_lumi(pad1, iPeriod, iPos)
        leg.Draw()

        pad2.cd()
        hratio.DrawCopy("E1")
        l.Draw("sames")

        c.Update()
        c.Print( outputdir + '/' + epoch + '/log/' + pngname )
        ###### end of log plots


    fileoutMC.Write()
    fileoutData.Write()
    fileoutMC.Close()
    fileoutData.Close()

######end of the function
