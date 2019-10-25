import os, sys

package_name: str = os.environ.get('gpAppPackageName') # com.studiowildcard.wardrumstudios.ark
device_id: int = int(os.environ.get('gsfDeviceId', 0))
device_codename: str = os.environ.get('gsfDeviceCodename')
auth_token: str = os.environ.get('gsfAuthToken')

if device_id == 0 or not device_codename or not auth_token or not package_name:
    print("Some of these environmental variables are missing: gsfDeviceId, gsfDeviceCodename, gsfAuthToken, gpAppPackageName")
    sys.exit(2)