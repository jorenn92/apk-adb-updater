import application
import yaml
from adb_shell.adb_device import AdbDeviceTcp, AdbDeviceUsb
from adb_shell.auth.sign_pythonrsa import PythonRSASigner

application = application.application

class device:
    name = ''
    ip = ''
    port = 5555
    enabled = True
    polling_time = 3600
    applications = []


    def __init__(self, vars):
        self.name = vars['name']
        self.ip = vars['ip']
        if(vars['enabled']):
            self.enabled = vars['enabled']
        if(vars['polling_time']):
            self.polling_time = vars['polling_time']
        if(vars['port']):
            self.port = vars['port']
        self.applications = []
        
        for app in vars['applications'] :
            self.applications.append(application(app))


    def load_devices():
        # Get configs
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file) 

        # set from config
        devices = config['devices']

        # get all devices
        all_devices = [];
        for dev in devices:
            all_devices.append(device(dev))
        return all_devices
    
    def connect_adb(self):
        # Load the public and private keys
        # Load the public and private keys
        adbkey = 'adb/keys'
        with open(adbkey) as f:
            priv = f.read()
        with open(adbkey + '.pub') as f:
            pub = f.read()

        signer = PythonRSASigner(pub, priv)
        device = AdbDeviceTcp(self.ip, 5555, default_transport_timeout_s=9.)
        device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        response1 = device.shell('echo TEST1')

    def adb_pair(self):
        # connect with a android 11+ device
        #adb pair <ip>:<port>
        # code ingeven
        response1 = device.shell('adb pair ' + self.ip + ':' + self.port)
