from typing import final

from pyasn1.type.univ import Null
from application import application
import yaml
import subprocess
import time
import os
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
from adb_shell.auth.keygen import keygen

class device:
    name = ''
    ip = ''
    port = 5555
    enabled = True
    timeout = 3600
    applications = []
    arch = 'arm64-v8a'
    dpi = 'nodpi'
    api_level = 0
    device_connection = Null

    def __init__(self, vars):
        self.name = vars['name']
        self.ip = vars['ip']
        if('enabled' in vars):
            self.enabled = vars['enabled']
        if('port' in vars):
            self.port = vars['port']
        if('arch' in vars):
            self.arch = vars['arch']
        if('dpi' in vars):
            self.dpi = vars['dpi']
        if('api_level' in vars):
            self.api_level = vars['api_level']
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
        i = 0
        while i < 3: 
            if i > 0:
                time.sleep(5)
                print('Retrying connection')

            out = self.connect_adb_now()
            if out == 1:
                return out
            else:
                i = i + 1
        print('Can\'t establish connection.. Giving up')

        
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
            print('For android versions < 11 a manual first pair is required.')
            return 0
    
    def connect_adb_now(self):
        # Load the public and private keys
        adbkey = 'config/keys/' + self.name + '/adb_key'

        try:
            with open(adbkey) as f:
                priv = f.read()
            with open(adbkey + '.pub') as f:
                pub = f.read()
            signer = PythonRSASigner(pub, priv)
        except FileNotFoundError:
            print('Keypair not found, generating new keys..')
            dirname = adbkey[::-1].split('/', 1)[1][::-1]
            os.makedirs(dirname)
            keygen(adbkey)
            print('Keys generated')
            return 0

        # Connect
        print('Connecting to ' + self.name)
        try:
            device = AdbDeviceTcp(self.ip, self.port, default_transport_timeout_s=9.0)
            device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
            print('Succesfully connected')
            self.device_connection = device
            return 1
        except Exception:
            print('Can\'t connect to the device right now')
            return 0

            
       

