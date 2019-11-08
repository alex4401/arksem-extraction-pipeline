import os, sys
from thirdparty.googleplayapi.gpapi.googleplay import GooglePlayAPI

from common import _gp_env as env

if len(sys.argv) <= 2:
    print("Usage: gp_download_blob.py BLOB_TYPE VERSION_CODE")
    sys.exit(1)

arg_blobType = sys.argv[1]
arg_version = int(sys.argv[2])

gapi = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename=env.device_codename)
gapi.login(gsfId=env.device_id, authSubToken=env.auth_token)
download_result = gapi.download(env.package_name, versionCode = arg_version, expansion_files = True)
for data_info in download_result['additionalData']:
    print(f'Found {data_info["type"]} (version = {data_info["versionCode"]})')
    if data_info["type"] != arg_blobType:
        print("- skipping")
        continue
    
    print("- downloading")
    with open(".".join([data_info["type"], str(data_info["versionCode"]), "blob"]), "wb") as file_handle:
        for chunk in data_info["file"]["data"]:
            file_handle.write(chunk)
