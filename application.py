
import urllib.request
import json
import shutil
import yaml
import subprocess
from providers.apkmirror import Apkmirror
from providers.aptoide import Aptoide
from providers.providerInterface import ProviderInterface
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb


class application:

    package_name = ''
    should_update = True
    latest_version = 0
    provider:ProviderInterface = Apkmirror()

    def __init__(self, vars):
        #self.url = vars['url']
        self.package_name = vars['package_name']
        if('should_update' in vars):
            self.should_update = vars['should_update']

        if('provider' in vars):
            if(str.lower(vars['provider']) == 'apkmirror'):
                self.provider = Apkmirror()
            else:
                self.provider = Aptoide()
        else:
            # Get from main config
            with open('config/config.yml', 'r') as file:
                config = yaml.safe_load(file) 
            if 'provider' in config:
                if(str.lower(config['provider']) == 'apkmirror'):
                    self.provider = Apkmirror()
                else:
                    self.provider = Aptoide()


    def latest_version(self):
        self.latest_version = self.provider.latest_app_version(self.package_name)
        return self.latest_version

    def get_from_api(self):
        return self.provider.request(self.package_name)


    def current_version(self, device):
        output = device.device_connection.shell('dumpsys package ' + self.package_name, transport_timeout_s=10.0, read_timeout_s=10.0, timeout_s=30.0, decode=True)
        pos = output.find('versionName')

        if pos != -1:
            str = output[pos:]
            posStart = str.find('=') + 1
            str = str[posStart:].partition('\n')[0].strip()
            return str
        else:
            return 0

    def download_apk(self, arch='arm64-v8a', dpi='nodpi', api_level=0):
        return self.provider.download_apk(self.package_name, self.latest_version, arch, dpi, api_level)

    def install_apk(self, device):
        apk_name = self.package_name +'_' + self.latest_version + '.apk'
        output = device.device_connection.shell('install -r cache/' + apk_name, transport_timeout_s=10.0, read_timeout_s=10.0, timeout_s=30.0, decode=True)
        print(output)
        if output.find('Success') != -1:
            return 1
        else:
            return 0





