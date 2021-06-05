#!/usr/bin/env bash

echo "Starting apk_adb_updater" 
echo "" > /opt/apk-adb-updater/logs/output.log
python3 -u /opt/apk-adb-updater/apk_updater.py 2>&1 | tee /opt/apk-adb-updater/logs/output.log