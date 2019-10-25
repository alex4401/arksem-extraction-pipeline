import os, sys
from thirdparty.googleplayapi.gpapi.googleplay import GooglePlayAPI

import .env

if len(sys.argv) <= 2:
    print("Usage: get-blob.py BLOB_TYPE VERSION_CODE")
    sys.exit(1)

arg_blobType = sys.argv[1]
arg_version = int(sys.argv[2])

gapi = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename=env.device_codename)
gapi.login(gsfId=env.device_id, authSubToken=env.auth_subtoken)
download_result = gapi.download(env.package_name, versionCode = arg_version, expansion_files = True)
for data_info in download_result['additionalData']:
    print(f'Found {data_info["type"]} (version = {data_info["versionCode"]}')
    if data_info["type"] != arg_blobType:
        print("- skipping")
        continue
    
    print("- downloading")
    with open(".".join([data_info["type"], str(data_info["versionCode"]), "blob"]), "wb") as file_handle:
        for chunk in data_info["file"]["data"]:
            file_handle.write(chunk)
