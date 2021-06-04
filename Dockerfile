FROM ubuntu:20.04
LABEL Maintainer="Jorenn92"
LABEL Description="Contains the apk-adb-updater image"

ENV     APP_HOME=/opt/apk-adb-updater/
ENV     LOG_DIR=/opt/apk-adb-updater/logs

RUN mkdir -p  ${APP_HOME}/config && \
    mkdir ~/.android

COPY    *.py                ${APP_HOME}
COPY    config/*            ${APP_HOME}/config/
COPY    entrypoint.sh       /

VOLUME ~/.android/

RUN set -x && \
    apt-get -y update  && \
    apt-get -y install pip python3 wget unzip  && \
    cd ${APP_HOME} && \
    pip install pyyaml requests adbutils && \
    mkdir -p adb/linux && \
    mkdir cache && \
    cd adb/linux && \
    wget --no-check-certificate https://dl.google.com/android/repository/platform-tools-latest-linux.zip && \
    unzip -o platform-tools-latest-linux.zip && \
    mv platform-tools/* . && \
    rm -rf platform-tools platform-tools-latest-linux.zip && \
    apt-get -y remove pip wget unzip && \
    chmod +x /entrypoint.sh


ENTRYPOINT ./entrypoint.sh