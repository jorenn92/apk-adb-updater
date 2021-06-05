import os
import glob
import sys
from time import sleep
from device import device
import time
from requests import get
import subprocess


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
                                state = application.download_apk(device.arch, device.dpi, device.api_level)
                                if state != 0:
                                    state = application.install_apk(device)
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
    # set working dir
    path = os.getenv('APP_HOME') if os.getenv('APP_HOME', '0') != '0' else None
    if path != None:
        os.chdir(path)

    # Go 
    platform_tools() # Update platform-tools
    devices = device.load_devices()
    if devices != 0:
        timeout = devices[0].timeout
        first_run = True
        while True :
            if(first_run != True):
                print('Done, updating again in ' + str(timeout) + ' seconds')
                time.sleep(timeout)
            else:
                if not(os.path.exists('cache') and os.path.isdir('cache')):
                    os.mkdir('cache', 0o755)
                first_run = False
            updater.perform_update(devices)
            clear_cache(), 
    else:
        time.sleep(3600)

def clear_cache():
    try:
        subprocess.call("rm -rf cache/*", shell=True)
    except Exception as e:
        print("Error: %s : %s" % (e.strerror))
    print('Cache cleared')

def platform_tools():
    print('Getting the latest Android Platform Tools..')
    # open in binary mode
    try:
        with open('cache/platform_tools.zip', "wb") as file:
            resp = get('https://dl.google.com/android/repository/platform-tools-latest-linux.zip')
            # write to file
            file.write(resp.content)
    except Exception: 
        print('Platform Tools update failed')
        return 0

    # install new
    try:
        import zipfile
        with zipfile.ZipFile('cache/platform_tools.zip', 'r') as zip_ref:
            zip_ref.extractall('cache/platform_tools')

            # remove previous install
        subprocess.call("rm -rf adb/linux/*", shell=True)
        subprocess.call("mv cache/platform_tools/platform-tools/* adb/linux/", shell=True)
        subprocess.call("chmod -R 755 adb/linux/*", shell=True)

        print('Platform Tools update complete')
        return 1
    except Exception:
        print('Platform Tools update failed')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
