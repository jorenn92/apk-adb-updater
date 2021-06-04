# Apk-adb-updater

Installs and keeps applications up to date on android devices in your local network through a remote adb connection. 
Periodically checks Aptoide or Apkmirror for an updated .apk and installs it on the device when an update is found.

Specifically build for updating a few applications on an android TV box which aren't available on the official play store, such as Google Chrome.

## Pairing your devices
Make sure you enable remote debugging in the developer settings of your device. 

### Android versions < 11
Configure your device with the default port '5555'. The updater will automatically make a connection and a popup will appear on the device. Make sure you 'always allow' the server. After that no further action is required. 

### Android versions >= 11
On the remote debugging screen, click on 'pair with code'. A popup will appear containing a pairing code and ip:port. 
Enter the auth_port & auth_code parameters in the device section of the config.yaml with above values where auth_port is the part after the ':' in the ip-address and auth_code is the Value shown under 'wifi pairing code'.

After that, restart the server. A connection should automatically be made. This should only be needed once, after that the auth_code & auth_port portions of the device config aren't required anymore. 

Note that the popup on the device won't stay forever, so you should quickly enter the values in the configuration and start the server to avoid having to try again.

Also, since android 11 the debug port isn't a fixed port anymore. It's now a random port which changes after toggling on / off the remote debug functionality. Make sure the correct port is entered in the configuration

##  Configuration

Configure all devices and applications in **config/config.yml**

```sh
  # EXAMPLE CONFIGURATION.. Change this
  devices: 
    - 
      applications: 
        - 
          package_name: "com.orange.be.orangetv"
          should_update: true
      enabled: true
      ip: "192.168.0.12"
      port: 43215 # optional
      name: Galaxy S10
      auth_port: 4586 # optional
      auth_code: 56325 # optional
    - 
      applications: 
        - 
          package_name: "com.android.chrome"
          should_update: true
        - 
          package_name: "com.google.android.apps.tv.launcherx"
          should_update: true
          provider: apkmirror # optional
      enabled: true
      ip: "192.168.0.6"
      port: 5555 # optional default = 5555
      name: shield
      arch: armeabi-v7a # optional
      api_level: 28 # optional
  timeout: 7200 # Check for updates every 2 hours
  provider: apkmirror # apkmirror | aptoide
```
## Running
```sh
python3 apk_updater.py
```
