import os, sys
from thirdparty.googleplayapi.gpapi.googleplay import GooglePlayAPI

if len(sys.argv) <= 1:
    print("Usage: pull-version-info.py OUTPUT_PATH")
    sys.exit(1)

arg_output = sys.argv[1]
if not 'gsfDeviceId' in os.environ and not 'deviceCodename' in os.environ and not 'authSubToken' in os.environ:
    print("Some of these environmental variables are missing: gsfDeviceId, deviceCodename, authSubToken")
    sys.exit(2)

gapi = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename=os.environ['deviceCodename'])
gapi.login(gsfId=int(os.environ['gsfDeviceId']), authSubToken=os.environ['authSubToken'])
app_details = gapi.details('com.studiowildcard.wardrumstudios.ark')
with open(arg_output, "w") as file_handle:
  file_handle.write(str(app_details['details']['appDetails']['versionCode']))
