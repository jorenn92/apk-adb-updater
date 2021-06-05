#!/usr/bin/env bash

echo "Starting apk_adb_updater" 
python3 -u /opt/apk-adb-updater/apk_updater.py 2>&1 | tee /opt/apk-adb-updater/logs/output.log

# docker run -d -v /usr/apps/apk-adb-updater/keys:/root/.android/ -v /usr/apps/apk-adb-updater/config:/opt/apk-adb-updater/config -v /usr/apps/apk-adb-updater/logs:/opt/apk-adb-updater/logs --net=host --name=apk-updater jorenn92/apk-adb-updater
