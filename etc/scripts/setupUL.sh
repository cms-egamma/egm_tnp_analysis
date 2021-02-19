#!bin/bash 

## add python lib
. /opt/rh/python27/enable
export LD_LIBRARY_PATH=/opt/rh/python27/root/usr/lib64/:$LD_LIBRARY_PATH

export PYTHONPATH=.:$PYTHONPATH
