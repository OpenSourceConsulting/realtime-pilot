#!/bin/bash
comp=$QUANT_HOME"/component"
cd $comp
pwd
python setup.py build_ext --inplace
cp -rf $QUANT_HOME"/component/component/*" $QUANT_HOME"/lib"