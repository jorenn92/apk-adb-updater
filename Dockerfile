FROM ubuntu:20.04
LABEL Maintainer="Jorenn92"
LABEL Description="Contains the apk-adb-updater image"

ENV     APP_HOME=/opt/apk-adb-updater/
ENV     LOG_DIR=/opt/apk-adb-updater/logs

RUN mkdir -p  ${APP_HOME}/config && \
    mkdir ${APP_HOME}/providers && \
    mkdir /root/.android

COPY    *.py                ${APP_HOME}
COPY    providers/*         ${APP_HOME}/providers/

COPY    config/*            ${APP_HOME}/config/
COPY    entrypoint.sh       /

VOLUME /root/.android/

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
    chmod 755 ${APP_HOME} && \
    chmod +x ${APP_HOME}/adb/linux/adb && \
    chmod +x /entrypoint.sh

ENTRYPOINT ./entrypoint.sh