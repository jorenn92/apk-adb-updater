from application import application
import yaml
import subprocess
import time
import os

class device:
    name = ''
    ip = ''
    port = 5555
    enabled = True
    timeout = 3600
    applications = []


    def __init__(self, vars):
        self.name = vars['name']
        self.ip = vars['ip']
        if(vars['enabled']):
            self.enabled = vars['enabled']
        if(vars['port']):
            self.port = vars['port']
        self.applications = []
        
        for app in vars['applications'] :
            self.applications.append(application(app))


    def load_devices():
        # Get configs
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
    
    def connect_adb(self):
        adb = subprocess.run(["adb/linux/adb", "devices"], stdout=subprocess.PIPE, text=True)
        # Do first pair if not found
        if adb.stdout.find(self.ip) == -1:
            if os.getenv('APP_HOME', None) != None:
                print('device ' + self.ip + ' not found. Starting first pair')
                state = self.adb_pair();
            else:
                print('Docker mode detected. At the moment it\'s not possible to automatically pair without user input. You need to exec in the container and adb pair your device manually before the updater wil do anything. Please check the documentation')
                print('Skipping the update for ' + device.name + '. Please pair manually')
        else:
            state = 1

        if state == 1:
            # Connect to device
            print('Connecting to ' + self.ip)
            adb = subprocess.run(["adb/linux/adb", "connect", str(self.ip) + ':' + str(self.port)], stdout=subprocess.PIPE)
            if (str(adb.stdout).find('connected to') != -1):
                print('Successfully connected')
                return 1
            else:
                print('Connection failed')
                return 0
        else:
            return 0

        
    def adb_pair(self):
        inp = input('is your device\'s android version >= 11 ? (y/n)')
        # For android 11+ do new pairing method
        if (inp == 'y' or inp == 'yes'):
            inp = input('Please enable remote debugging and pair device with code. Please enter the pairing port(underneath the code, after the ip:) and generated code, split by a \',\' (i.e. 5542,698796): ')
            pos = inp.find(',')
            adb = subprocess.run(["adb/linux/adb", "pair", self.ip + ':' + inp[:pos]], stdout=subprocess.PIPE, text=True, input=inp[pos + 1:])
            if adb.stdout.find('Successfully paired') != -1:
                print('Pairing..')
                time.sleep(5)
                print('Successfully paired to ' + self.name)
                return 1
            else:
                print('Device not found.. ')
                return 0
        else:
            # For android 10 and lower.. Do older method which requires cable
            print('For android versions < 11 a first pair with cable is required. This is sadly not implemented yet.')
            return 0
