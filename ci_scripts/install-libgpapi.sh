#!/bin/bash

if [[ -d /job_shared/lib_gpapi ]]
then
    echo "No need to build Google Play API library again."
    exit 0
fi

git submodule update --init thirdparty/googleplayapi
cd thirdparty/googleplayapi
python setup.py build
cd ../..
mv thirdparty/googleplayapi /job_shared/lib_gpapi