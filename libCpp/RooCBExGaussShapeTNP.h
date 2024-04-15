#ifndef ROO_CB_EX_GAUSS_SHAPE_TNP
#define ROO_CB_EX_GAUSS_SHAPE_TNP


#include "RooAbsPdf.h"
#include "RooAbsArg.h"
#include "RooRealProxy.h"
#include "RooRealVar.h"
#include "RooCategoryProxy.h"
#include "RooAbsReal.h"
#include "RooAbsCategory.h"
#include "TMath.h"
#include "Riostream.h"

class RooCBExGaussShapeTNP : public RooAbsPdf {
public:
  RooCBExGaussShapeTNP() {} ; 
  RooCBExGaussShapeTNP(const char *name, const char *title,
		    RooAbsReal& _m,
		    RooAbsReal& _m0,
		    RooAbsReal& _sigma,
		    RooAbsReal& _alpha,
		    RooAbsReal& _n,
		    RooAbsReal& _sigma_2,
		    RooAbsReal& _tailLeft

		    );

  RooCBExGaussShapeTNP(const RooCBExGaussShapeTNP& other, const char* name);
  inline virtual TObject* clone(const char* newname) const { return new RooCBExGaussShapeTNP(*this,newname);}
  inline ~RooCBExGaussShapeTNP(){}
  Double_t evaluate() const ;
  
  ClassDef(RooCBExGaussShapeTNP, 2)

protected:

  RooRealProxy m ;
  RooRealProxy  m0 ;
  RooRealProxy  sigma ;
  RooRealProxy  alpha ;
  RooRealProxy  n ;
  RooRealProxy  sigma_2 ;
  RooRealProxy tailLeft ;
    
};

#endif
