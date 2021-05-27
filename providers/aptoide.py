import urllib.request
import json
import shutil
from providers.providerInterface import ProviderInterface

class Aptoide(ProviderInterface):
    api_url='http://ws75.aptoide.com/api/7/apps/'

    def request(self, package_name):
        url = self.api_url + 'search?query=' + package_name;

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        response = json.loads(data)    

        for app in response['datalist']['list']:
            if app['package'] == package_name:
                return app 
        return 0

    def latest_app_version(self, package_name):
        api_resp = self.request(package_name)
        if api_resp != 0 :
            self.latest_version = api_resp['file']['vername']
            return api_resp['file']['vername'].strip()
        else : 
            return 0 

    def download_apk(self, package_name, version, arch='arm64-v8a', dpi='nodpi', api_level=0):
        app = self.request(package_name)
        # download the latest apk from aptoide
        with urllib.request.urlopen(app['file']['path']) as response, open('cache/' + package_name +'_' + version  +'.apk', 'wb') as out_file:
            shutil.copyfileobj(response, out_file)
        return 1