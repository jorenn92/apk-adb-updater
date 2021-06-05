from application import application
import yaml
import subprocess
import time
import adbutils

class device:
    name = ''
    ip = ''
    port = str(5555)
    enabled = True
    timeout = 3600
    applications = []
    arch = 'arm64-v8a'
    dpi = 'nodpi'
    api_level = 0
    auth_port = ''
    auth_code = ''
    adb_server_host = '127.0.0.1'
    adb_server_port = 5037
    
    def __init__(self, vars):
        self.name = vars['name']
        self.ip = vars['ip']
        if('enabled' in vars):
            self.enabled = vars['enabled']
        if('port' in vars):
            self.port = str(vars['port'])
        if('arch' in vars):
            self.arch = vars['arch']
        if('dpi' in vars):
            self.dpi = vars['dpi']
        if('api_level' in vars):
            self.api_level = vars['api_level']
        if('auth_code' in vars):
            self.auth_code = str(vars['auth_code'])
        if('auth_port' in vars):
            self.auth_port = str(vars['auth_port'])
        self.applications = []
        
        for app in vars['applications'] :
            self.applications.append(application(app))


    def load_devices():
        # Get configs
        try:
            with open('config/config.yml', 'r') as file:
                config = yaml.safe_load(file) 
            
            # set from config
            devices = config['devices']

            # get all devices
            all_devices = [];
            for dev in devices:
                dev = device(dev)
                dev.timeout = config['timeout']
                all_devices.append(dev)
            return all_devices
        except Exception:
            print('Failed loading devices or no device found. Please check your config.yml')
            return 0
    
    def connect_adb(self):
        i=0
        while i < 5:
            state = self.try_adb_connection()
            if state == 1:
                return 1 
            else:
                if i < 4:
                    time.sleep(2)
                    i=i+1
                else:
                    print('Connection failed. Please check your device for a popup. Android versions > 11 should reboot the server with auth_port & auth_code')
                    return 0
            
    def try_adb_connection(self):
        subprocess.run(["adb/linux/adb", "start-server"], stdout=subprocess.PIPE, text=True)
        adb = adbutils.AdbClient(host=self.adb_server_host, port=self.adb_server_port)
        output = adb.connect(self.ip + ':' + self.port, timeout=30.0)
        if output.find('failed to connect') == 0:
            if self.auth_port != '' and self.auth_code != '':
                print('Performing first pair with port ' + self.auth_port + ' and code ' + self.auth_code)
                self.adb_pair(self.auth_port,self.auth_code);
                output = adb.connect(self.ip + ':' + self.port, timeout=30.0)
                if self.adb_status() == 1:
                    print('Connection succesfull')
                    return 1
            else:
                return 0
        else:
            if self.adb_status() == 1:
                print('Connection succesfull')
                return 1
            else:
                return 0                    
        
    def adb_pair(self, port, code):
        # For android 11+ do new pairing method
        adb = subprocess.run(["adb/linux/adb", "pair", self.ip + ':' + port], stdout=subprocess.PIPE, text=True, input=code)
        if adb.stdout.find('Successfully paired') != -1:
            print('Pairing..')
            time.sleep(5)
            print('Successfully paired to ' + self.name)
            return 1
        else:
            print('Device not found.. ')
            return 0

    def adb_status(self):
        adb = adbutils.AdbClient(host=self.adb_server_host, port=self.adb_server_port)
        devices = adb.device_list()

        for adbdevice in devices:
            if adbdevice.serial.find(self.ip) == 0:
                return 1    
        return 0