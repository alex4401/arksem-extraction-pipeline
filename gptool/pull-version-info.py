from thirdparty.googleplayapi.gpapi.googleplay import GooglePlayAPI

import .env

gapi = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename=env.device_codename)
gapi.login(gsfId=env.device_id, authSubToken=env.auth_subtoken)
app_details = gapi.details(env.package_name)
print(app_details['details']['appDetails']['versionCode'])