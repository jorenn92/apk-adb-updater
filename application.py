
import urllib.request
import json
import shutil

class application:

    api_url = 'http://ws75.aptoide.com/api/7/apps/'
    name = ''
    should_update = True
    latest_version = 0

    def __init__(self, vars):
        #self.url = vars['url']
        self.name = vars['name']
        if(vars['should_update']):
            self.should_update = vars['should_update']


    def get_from_api(self):
        url = self.api_url + 'search?query=' + self.name;

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        response = json.loads(data)    

        for app in response['datalist']['list']:
            if app['uname'] == self.name:
                return app 
        return 0

    def latest_version(self):
        api_resp = self.get_from_api()
        if api_resp != 0 :
            self.latest_version = api_resp['file']['vername']
            return api_resp['file']['vername']
        else : 
            return 0


    def download_apk(self):
        app = self.get_from_api()
        # download the latest apk from aptoide
        with urllib.request.urlopen(app['file']['path']) as response, open('temp/' + self.name +'_' + self.latest_version  +'.apk', 'wb') as out_file:
            shutil.copyfileobj(response, out_file)


