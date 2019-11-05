#!/bin/bash
if [[ `cat /ram/APK_VERSION` == `cat /job_shared/LAST_APK_VERSION` ]]; then
  echo "No need to update the data."
  exit 1
fi

mv /ram/APK_VERSION /job_shared/LAST_APK_VERSION
exit 0