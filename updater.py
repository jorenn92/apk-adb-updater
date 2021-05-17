import yaml
from device import device



devices = device.load_devices()
print(devices)
# for each device

for device in devices:
    print('Starting update for ' + device.name)
    # check if device is available
    connected = device.connect_adb()
    # if available
        # connect device
        # if connection = success
        # loop applications
    for application in device.applications:
        print('Updating ' + application.name)
        # if application installed on device
            # check current version on device
        # get newest version from url
        latest_version = application.latest_version()
        if latest_version != 0:
            print('downloading version ' + latest_version)
            application.download_apk()
            # if newest version != current version
                # install newest version
        else :
            print ('Application not found.. Make sure the correct aptoide name is used')
    
        # else : application not installed on device
            # install newest version



