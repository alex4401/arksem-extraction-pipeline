FROM jfloff/alpine-python:3.7-slim
RUN apk add unzip protobuf \
            py3-requests py3-cryptography &&\
    rm -rf /var/cache/apk/*

ADD requirements.txt /requirements.txt
RUN pip install --user --no-cache-dir protobuf &&\
    rm -rf /var/cache/apk/* &&\
    rm /requirements.txt