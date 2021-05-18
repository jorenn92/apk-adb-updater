import sys
from device import device
import yaml

class updater:
    def perform_update(devices):
        for device in devices:
            if device.enabled == True:
                print('Starting update for ' + device.name)
                # pair and connect device
                connected = device.connect_adb()

                # connection success.. loop applications
                if connected == 1:
                    for application in device.applications:
                        if application.should_update == True:
                            current_ver = application.current_version(device)
                            latest_version = application.latest_version()

                            # get newest version from url
                            if current_ver != 0:
                                print('Detected installed ' + application.package_name +' version ' + current_ver)
                            else:
                                print(application.package_name + ' not installed yet')

                            # install newer version if other version detected
                            if latest_version != 0 and latest_version != current_ver:
                                print('Installing version ' + latest_version + '...')
                                application.download_apk()
                                state = application.install_apk()
                                if state != 0:
                                    print('succesfully installed ' + application.package_name + ' version ' + latest_version)
                                else :
                                    print('installation of ' + application.package_name + ' version ' + latest_version + ' failed')
                            else :
                                print ('no upgrade needed for ' + application.package_name)
                else:
                    print('Device not available. Skipping ' + device.name)
            else:
                print(device.name + ' isn\'t enabled. Skipping..')


def main(args=None):
    devices = device.load_devices()
    updater.perform_update(devices)

if __name__ == "__main__":
    sys.exit(main())