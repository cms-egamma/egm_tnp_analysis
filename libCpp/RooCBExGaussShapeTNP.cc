#include "RooCBExGaussShapeTNP.h" 

ClassImp(RooCBExGaussShapeTNP) 

RooCBExGaussShapeTNP::RooCBExGaussShapeTNP(const char *name, const char *title, 
				     RooAbsReal& _m,
				     RooAbsReal& _m0,
				     RooAbsReal& _sigma,
				     RooAbsReal& _alpha,
				     RooAbsReal& _n,
				     RooAbsReal& _sigma_2,
				     RooAbsReal& _tailLeft
				     ) :
RooAbsPdf(name,title), 
  m("m","m",this,_m),
  m0(" m0"," m0",this,_m0),
  sigma(" sigma"," sigma",this,_sigma),
  alpha(" alpha"," alpha",this,_alpha),
  n(" n"," n",this,_n),
  sigma_2(" sigma_2"," sigma_2",this,_sigma_2),
  tailLeft(  " tailL"," tailL",this,_tailLeft)

{}

RooCBExGaussShapeTNP::RooCBExGaussShapeTNP(const RooCBExGaussShapeTNP& other, const char* name):
  RooAbsPdf(other,name), 
  m("m",this,other.m),
  m0(" m0",this,other. m0),
  sigma(" sigma",this,other. sigma),
  alpha(" alpha",this,other. alpha),
  n(" n",this,other. n),
  sigma_2(" sigma_2",this,other. sigma_2),
  tailLeft(" tailL",this,other.tailLeft)

{}


Double_t RooCBExGaussShapeTNP::evaluate() const 
{ 
  Double_t rval=0;

  Double_t t = (m-m0)/sigma;
  Double_t t0 = (m-m0)/sigma_2;
  // if (alpha < 0){ 
  //   t = -t;
  //   t0 = -t0;
  // }

  Double_t absAlpha = fabs((Double_t)alpha);
  if( tailLeft >= 0 ) {
    if (t>0) {
      rval= exp(-0.5*t0*t0);
    }
    else if (t > -absAlpha) {
      rval= exp(-0.5*t*t);
    }
    else {
      //      Double_t a =  TMath::Power(n/absAlpha,n)*exp(-0.5*absAlpha*absAlpha);
      //      Double_t b= n/absAlpha - absAlpha; 
      //      rval= a/TMath::Power(b - t, n);
      Double_t a = exp(-0.5*absAlpha*absAlpha);
      Double_t b = exp(n*(t+absAlpha));
      rval = a*b;
    }
  } else {
    //// rather fit high tail for n < 0
    if (t0<0) {
      rval= exp(-0.5*t*t);
    }
    else if (t0 < absAlpha) {
      rval= exp(-0.5*t0*t0);
    }
    else {
      Double_t absN = fabs((Double_t) n );
      Double_t a =  TMath::Power(absN/absAlpha,absN)*exp(-0.5*absAlpha*absAlpha);
      Double_t b= absN/absAlpha - absAlpha;
      rval= a/TMath::Power(b + t0, absN);
    }

  }

  return rval;
} 
