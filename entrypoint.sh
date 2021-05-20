#!/usr/bin/env bash

# Start adb daemon
/opt/aptoide-adb-updater/adb/linux/adb start-server

echo "Starting aptoide_adb_updater" 
python3 /opt/aptoide-adb-updater/aptoide_updater.py 2>&1 | tee /opt/aptoide-adb-updater/logs/output.log