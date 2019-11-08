from thirdparty.googleplayapi.gpapi.googleplay import GooglePlayAPI

from common import _gp_env as env

gapi = GooglePlayAPI(locale="en_US",
                     timezone="UTC",
                     device_codename=env.device_codename)
gapi.login(gsfId=env.device_id, authSubToken=env.auth_token)
app_details = gapi.details(env.package_name)
print(app_details['details']['appDetails']['versionCode'])
