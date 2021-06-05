
import yaml
import subprocess
from providers.apkmirror import Apkmirror
from providers.aptoide import Aptoide
from providers.providerInterface import ProviderInterface


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
        adb = subprocess.run(["adb/linux/adb", "-s", device.ip + ':' + device.port, "shell", "dumpsys", "package", self.package_name], stdout=subprocess.PIPE, text=True)
        pos = adb.stdout.find('versionName')
        if pos != -1:
            str = adb.stdout[pos:]
            posStart = str.find('=') + 1
            str = str[posStart:].partition('\n')[0].strip()
            return str
        else:
            return 0

    def download_apk(self, arch='arm64-v8a', dpi='nodpi', api_level=0):
        return self.provider.download_apk(self.package_name, self.latest_version, arch, dpi, api_level)

    def install_apk(self, device):
        try:
            apk_name = self.package_name +'_' + self.latest_version + '.apk'
            adb = subprocess.run(["adb/linux/adb", "-s", device.ip + ':' + device.port, "install", "-r", "cache/" + apk_name], stdout=subprocess.PIPE, text=True)
            if adb.stdout.find('Success') != -1:
                return 1
            else:
                return 0
        except Exception:
            print('Installation failed. Please note that it\'s currently not possible to install app bundles. Only apk\'s are supported')





