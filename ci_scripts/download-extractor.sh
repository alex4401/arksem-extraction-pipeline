#!/bin/bash
if [[ -f "$1/UDE_VERSION" && -f "$1/ude-debug.arm" ]]
then
    if [[ `cat "$1/UDE_VERSION"` == $UDE_VERSION ]]
    then
        echo "No need to download the extractor: v$UDE_VERSION is already present at the location."
        exit 0
    fi
fi

curl https://github.com/alex4401/ude/releases/download/$UDE_VERSION/ude-debug.arm --output "$1/ude-debug.arm"
echo $UDE_VERSION > "$1/UDE_VERSION"