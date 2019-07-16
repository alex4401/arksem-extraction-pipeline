import os, sys
from thirdparty.googleplayapi.gpapi.googleplay import GooglePlayAPI

if not 'gsfDeviceId' in os.environ and not 'deviceCodename' in os.environ and not 'authSubToken' in os.environ:
    print("Some of these environmental variables are missing: gsfDeviceId, deviceCodename, authSubToken")
    sys.exit(1)

gapi = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename=os.environ['deviceCodename'])
gapi.login(gsfId=int(os.environ['gsfDeviceId']), authSubToken=os.environ['authSubToken'])
download_result = gapi.download('com.studiowildcard.wardrumstudios.ark', expansion_files = True)
for data_info in download_result['additionalData']:
    print(data_info["type"], data_info["versionCode"])
    with open(".".join([data_info["type"], str(data_info["versionCode"]), "bin"]), "wb") as file_handle:
        for chunk in data_info["file"]["data"]:
            file_handle.write(chunk)