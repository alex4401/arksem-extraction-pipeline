#!/bin/bash
sed -i 's/^.*\(LogPakFile.*" \).*$/\1/' $1
sed -i 's/LogPakFile: Display: //g' $1
sed -i 's/"//g' $1
