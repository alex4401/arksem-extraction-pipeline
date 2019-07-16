import sys
from thirdparty.googleplayapi.gpapi.googleplay import GooglePlayAPI

if len(sys.argv) < 3:
    print("Usage: auth-fake-device.py $email $password [$device=marlin]")
    sys.exit(1)

arg_email = sys.argv[1]
arg_password = sys.argv[2]
arg_device = sys.argv[3] if len(sys.argv) >= 4 else "sailfish"

gapi = GooglePlayAPI(locale="en_US", timezone="UTC", device_codename=arg_device)
gapi.login(email=arg_email, password=arg_password)

print(gapi)
print(gapi.gsfId)
print(gapi.authSubToken)
