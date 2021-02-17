#!bin/bash 

if [[ `uname -n` == *"lxplus"* ]]; then 
## install gcc 4.9
    optVer=x86_64-slc6-gcc49-opt
    optVer=x86_64-slc6-gcc48-opt

## install modern version of ROOT
    LCG=/afs/cern.ch/sw/lcg/
    ROOTSYS=$LCG/app/releases/ROOT/6.06.06/$optVer/root/
    . $LCG/external/gcc/4.8.0/$optVer/setup.sh
    . $ROOTSYS/bin/thisroot.sh

fi

export PYTHONPATH=.:$PYTHONPATH

### add pypyroot
#. /afs/.cern.ch/sw/lcg/external/pypy/x86_64-slc6/setup-pypyroot.sh