# aptoide-adb-updater

Installs and keeps applications up to date on android 11+ devices in your local network through a remote adb connection. 
Periodically checks Aptoide for an updated .apk and installs it on the device when an update is found.

Specifically build for updating a few applications on an android TV box which aren't available on the official play store, such as Google Chrome.

It is possible to also use the updater on devices with Android versions < 11 through manually pairing. You'll need to connect the device with a cable once and follow [these instructions](https://developer.android.com/studio/command-line/adb#wireless). But once it is paired and it shows up in 'adb devices' the updater should find the device and install/update the applications. 

**Currently an adb pair is needed after each restart of the adb daemon which isn't ideal.**

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
      port: 43215
      name: Galaxy S10
    - 
      applications: 
        - 
          package_name: "com.android.chrome"
          should_update: true
        - 
          package_name: "com.google.android.apps.tv.launcherx"
          should_update: true
          provider: apkmirror
      enabled: true
      ip: "192.168.0.6"
      port: 5555
      name: shield
      arch: armeabi-v7a
      api_level: 28
  timeout: 7200 # Check for updates every 2 hours
  provider: apkmirror # apkmirror | aptoide
```
## Running
```sh
python3 aptoide_updater.py
```
