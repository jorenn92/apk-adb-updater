# Apk-adb-updater

Installs and keeps applications up to date on android devices in your local network through a remote adb connection. 
Periodically checks Aptoide or Apkmirror for an updated .apk and installs it on the device when an update is found.

Specifically build for updating a few applications on an android TV box which aren't available on the official play store, such as Google Chrome.

It is recommended to manually pair your device with remote adb. When your device is available in 'adb devices' the updater will pick it up.
There's also a build in way to pair with android 11+. (user action still required)

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
python3 apk_updater.py
```
