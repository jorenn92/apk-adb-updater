FROM ubuntu:20.04
LABEL Maintainer="Jorenn92"
LABEL Description="Contains the aptoid-adb-updater image"

ENV APP_HOME=/opt/aptoide-adb-updater/

RUN  mkdir -p  ${APP_HOME}/config

COPY    *.py                ${APP_HOME}
COPY    config/*            ${APP_HOME}/config/
COPY    entrypoint.sh       /

RUN set -x && \
    apt-get -y update  && \
    apt-get -y install pip python3 wget unzip  && \
    cd ${APP_HOME} && \
    pip install pyyaml && \
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