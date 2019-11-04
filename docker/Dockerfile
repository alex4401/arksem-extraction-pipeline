FROM python:3.5.8-alpine3.10

ENV PACKAGES="\
      dumb-init \
      bash \
      ca-certificates \
      protobuf \
      curl \
    "
ENV BUILD_PACKAGES="\
      bzip2-dev \
      coreutils \
      dpkg-dev dpkg \
      expat-dev \
      findutils \
      gcc \
      gdbm-dev \
      libc-dev \
      libffi-dev \
      libnsl-dev \
      libtirpc-dev \
      linux-headers \
      make \
      ncurses-dev \
      libressl-dev \
      pax-utils \
      readline-dev \
      sqlite-dev \
      tcl-dev \
      tk \
      tk-dev \
      util-linux-dev \
      xz-dev \
      zlib-dev \
      git \
    "

RUN apk add --no-cache $PACKAGES && \
    rm -rf /var/cache/apk/*
RUN apk add --no-cache --virtual=.build-dependencies $BUILD_PACKAGES wget ca-certificates   && \
    pip3 install --no-cache-dir cryptography protobuf requests              && \
    apk del --no-cache --purge .build-dependencies                                  && \
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/usr/bin/dumb-init", "bash", "-l", "-c"]
