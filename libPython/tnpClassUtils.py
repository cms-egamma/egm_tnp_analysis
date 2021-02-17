import copy
import os

def mkdir(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory) 

class tnpSample:
    def __init__(self, sName, path, cut = None, lumi = -1, nEvts = -1, mcTruth = False, puTree = None, isMC = False ):
        self.path = []
        self.name = sName
        self.path.append(path)
        self.cut     = cut
        self.lumi    = lumi
        self.nEvts   = nEvts
        self.mcTruth = mcTruth
        self.puTree  = puTree
        self.isMC    = isMC
        self.weight  = None
        self.tnpTree = None
        self.maxWeight = 999999

    def set_weight(self,weight):
        self.weight = weight

    def set_maxWeight(self, maxi):
        self.maxWeight = maxi
    
    def set_tnpTree( self, treename):
        self.tnpTree = treename

    def set_puTree(self,puTree):
        self.puTree = puTree

    def set_cut(self,cut):
        self.cut = cut
    
    def set_mcTruth(self,truth = True):
        self.mcTruth = truth

    def dump(self):
        print '**** name: %-*s ' % (100, self.name)
        print '  path    : ', self.path
        print '  tnpTree : ', self.tnpTree
        if self.isMC:
            print '   --- MC sample --- '
            print '  nEvts    : ', self.nEvts
            print '  mcTruth  : ', self.mcTruth
            print '  puTree   : ', self.puTree
            print '  weight   : ', self.weight
        else  :
            print '   --- Data sample --- '
            print '  lumi     : ', self.lumi

    def rename(self, newname):
        self.name = newname
    
    def clone(self):
        return copy.deepcopy(self)


    def add_sample(self, sample):
        if self.lumi >= 0  :
            self.lumi = self.lumi + sample.lumi
        if self.nEvts >= 0 :
            self.nEvts = self.nEvts + sample.nEvts
        self.path.extend( sample.path )




import ROOT as rt
iHistUnique = 0

class tnpVar:
    def __init__(self, var, hname = None, title = None, xmin = 0, xmax = 0, nbins = -1, cut = None ):
        self.var   = var
        if title is None :  self.title = var
        else:               self.title = title
        self.xmin  = xmin
        self.xmax  = xmax
        self.nbins = nbins
        self.hname = hname
        self.hist  = None
        self.cut   = None

    def get_hist(self):
        if self.nbins > 0 and self.hist is None:
            if self.hname is None:
                global iHistUnique
                self.hname  = 'h_%s_%d' % (self.var,iHistUnique)
                iHistUnique += 1
            self.hist  = rt.TH1F( self.hname, self.title, 
                                  self.nbins, self.xmin, self.xmax )
            self.hist.GetXaxis().SetTitle(self.title)
            self.hist.SetMinimum(0)
            self.hist.Sumw2()

        return self.hist

    def varName(self):
        return self.var
    
    def set_hname(self,name):
        self.hname = name


