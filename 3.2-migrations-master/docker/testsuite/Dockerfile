FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y \
            python3.8 python3-virtualenv \
            postgresql-client && \
    apt-get clean

RUN mkdir -p /opt/yandex
RUN python3 -m virtualenv --python=/usr/bin/python3 /opt/yandex/testsuite

RUN mkdir -p /tmp/testsuite

COPY requirements.txt /tmp/requirements.txt
RUN /opt/yandex/testsuite/bin/pip install -r /tmp/requirements.txt
