#!/bin/bash
if [[ -d /job_shared/$1 ]]; then
    echo "$1 located in the job cache."
    exit 0
fi

exit 1