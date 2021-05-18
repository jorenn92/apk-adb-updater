# aptoide-adb-updater

example configuration: 

devices: 
  - 
    applications: 
      - 
        package_name: "com.android.chrome"
        should_update: true
      - 
        package_name: "com.orange.be.orangetv"
        should_update: true
    enabled: true
    ip: "192.168.0.12"
    port: 43215
    name: shield
    polling_time: 3600
  - 
    applications: 
      - 
        package_name: "com.android.chrome"
        should_update: true
    enabled: true
    ip: "192.168.0.8"
    port: 5555
    name: "Galaxy S10"
    polling_time: 3600