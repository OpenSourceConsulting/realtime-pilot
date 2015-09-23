#!/bin/bash
rm -rf build
rm -rf component
rm -rf ../lib/ServiceClass.so
python setup.py build_ext --inplace
cp -rf component/ServiceClass.so ../lib/ServiceClass.so
