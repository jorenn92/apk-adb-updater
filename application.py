
import urllib.request
import json
import shutil
import subprocess


class application:

    api_url = 'http://ws75.aptoide.com/api/7/apps/'
    package_name = ''
    should_update = True
    latest_version = 0

    def __init__(self, vars):
        #self.url = vars['url']
        self.package_name = vars['package_name']
        if(vars['should_update']):
            self.should_update = vars['should_update']


    def get_from_api(self):
        url = self.api_url + 'search?query=' + self.package_name;

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        response = json.loads(data)    

        for app in response['datalist']['list']:
            if app['package'] == self.package_name:
                return app 
        return 0

    def latest_version(self):
        api_resp = self.get_from_api()
        if api_resp != 0 :
            self.latest_version = api_resp['file']['vername']
            return api_resp['file']['vername'].strip()
        else : 
            return 0

    def current_version(self, device):
        adb = subprocess.run(["adb/linux/adb", "shell", "dumpsys", "package", self.package_name], stdout=subprocess.PIPE, text=True)
        pos = adb.stdout.find('versionName')
        if pos != -1:
            str = adb.stdout[pos:]
            posStart = str.find('=') + 1
            str = str[posStart:].partition('\n')[0].strip()
            return str
        else:
            return 0

    def download_apk(self):
        app = self.get_from_api()
        # download the latest apk from aptoide
        with urllib.request.urlopen(app['file']['path']) as response, open('cache/' + self.package_name +'_' + self.latest_version  +'.apk', 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

    def install_apk(self):
        apk_name = self.package_name +'_' + self.latest_version + '.apk'
        adb = subprocess.run(["adb/linux/adb", "install", "-r", "cache/" + apk_name], stdout=subprocess.PIPE, text=True)
        print(adb.stdout)
        if adb.stdout.find('Success') != -1:
            return 1
        else:
            return 0





