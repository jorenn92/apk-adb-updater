import urllib.request
from requests import get
import json
from providers.providerInterface import ProviderInterface

class Apkmirror(ProviderInterface):
    api_url='https://www.apkmirror.com'
    userAgent = 'APKUpdater-v2.0.5'
    creds = 'YXBpLWFwa3VwZGF0ZXI6cm01cmNmcnVVakt5MDRzTXB5TVBKWFc4'

    def request(self, package_name):
        api_path='/wp-json/apkm/v1/app_exists/'
        url = self.api_url + api_path;

        req = urllib.request.Request(url)
        req.add_header('User-Agent', self.userAgent)
        req.add_header("Authorization", "Basic %s" % self.creds)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        data = json.dumps({"pnames": [package_name], "exclude": ["beta", "alpha"]}).encode('utf-8')
        req.add_header('Content-Length', len(data))
        response = urllib.request.urlopen(req, data)
        data = response.read()
        return json.loads(data)

    def latest_app_version(self, package_name):
        api_resp = self.request(package_name)
        if api_resp != 0 :
            if api_resp['data'][0]['exists'] != False:
                return api_resp['data'][0]['release']['version']
            else:
                print(package_name + ' doesn\'t exist on Apkmirror')
                return 0
        else : 
            return 0 

    def download_apk(self, package_name, version, arch='arm64-v8a', dpi='nodpi', api_level=0):
        app = self.request(package_name)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}
        
        # download the latest apk 
        link = self.get_link(app, arch, dpi, api_level)
        if link != 0 :
            resp = get(link, allow_redirects=True, headers=headers)
            id = resp.content.decode("utf-8").split('/wp-content/themes/APKMirror/download.php?id=')[1].split('"')[0]
            # open in binary mode
            with open('cache/' + package_name +'_' + version  + '.apk', "wb") as file:
            # get request
                resp = get(self.api_url + '/wp-content/themes/APKMirror/download.php?id=' + id, headers=headers)
                # write to file
                file.write(resp.content)
        else:
            return 0

    def get_link(self, api_resp, arch='arm64-v8a', dpi='nodpi', api_level=0, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}):
        for apk in api_resp['data'][0]['apks'] :
            if arch in apk['arches'] or len(apk['arches']) < 1 :
                if 'minapi' in apk and (int(api_level) >= int(apk['minapi']) or int(api_level) == 0):
                    if dpi in apk['dpis'] or dpi == 'nodpi':
                        link= self.api_url + apk['link']
                        resp = get(link, allow_redirects=True, headers=headers)
                        # Skip if it's an apk bundle
                        if(resp.content.decode("utf-8").find('What\'s inside this APK bundle?') == -1):
                            # Return the download ID
                            return self.api_url + apk['link'] + 'download/'
        print('no suitable .apk found for given architecture, dpi & min version. Note: we can\'t install split apk\'s')
        return 0

