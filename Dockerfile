FROM ubuntu:20.04
LABEL Maintainer="Jorenn92"
LABEL Description="Contains the aptoid-adb-updater image"

ENV APP_HOME=/opt/aptoide-adb-updater/

RUN groupadd user && \
    useradd -g user user && \
    mkdir -p ${APP_HOME} && \
    chown -R user:user ${APP_HOME}

COPY    --chown=user:user   *.py                ${APP_HOME}
COPY    --chown=user:user   config.yml          ${APP_HOME}
COPY    --chown=user:user   entrypoint.sh     /

RUN set -x && \
    apt-get -y update  && \
    apt-get -y install pip python3 wget unzip  && \
    cd ${APP_HOME} && \
    pip install pyyaml && \
    mkdir -p adb/linux && \
    mkdir cache && \
    cd adb/linux && \
    wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip && \
    unzip -o platform-tools-latest-linux.zip && \
    mv platform-tools/* . && \
    rm -rf platform-tools platform-tools-latest-linux.zip && \
    apt-get -y remove pip wget unzip && \
    chown -R user:user ${APP_HOME} && \
    chown user:user /entrypoint.sh && \
    chmod +x /entrypoint.sh

USER user
ENTRYPOINT ./entrypoint.sh