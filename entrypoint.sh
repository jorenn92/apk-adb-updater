#!/usr/bin/env bash

echo "Starting apk_adb_updater" 
python3 /opt/apk-adb-updater/apk_updater.py 2>&1 | tee /opt/apk-adb-updater/logs/output.log