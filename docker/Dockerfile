FROM alpine:3.10

ENV LANG=C.UTF-8

# Here we install GNU libc (aka glibc) and set C.UTF-8 locale as default.

ENV ALPINE_GLIBC_BASE_URL="https://github.com/sgerrand/alpine-pkg-glibc/releases/download" \
    ALPINE_GLIBC_PACKAGE_VERSION="2.29-r0" \
    PYTHON_VERSION=3.7.3

ENV ALPINE_GLIBC_BASE_PACKAGE_FILENAME="glibc-$ALPINE_GLIBC_PACKAGE_VERSION.apk" \
    ALPINE_GLIBC_BIN_PACKAGE_FILENAME="glibc-bin-$ALPINE_GLIBC_PACKAGE_VERSION.apk" \
    ALPINE_GLIBC_I18N_PACKAGE_FILENAME="glibc-i18n-$ALPINE_GLIBC_PACKAGE_VERSION.apk"

ENV PYTHON_PATH=/usr/local/bin/ \
    PATH="/usr/local/lib/python$PYTHON_VERSION/bin/:/usr/local/lib/pyenv/versions/$PYTHON_VERSION/bin:${PATH}" \
    # These are always installed. Notes:
    #   * dumb-init: a proper init system for containers, to reap zombie children
    #   * bash: For entrypoint, and debugging
    #   * ca-certificates: for SSL verification during Pip and easy_install
    PACKAGES="\
      dumb-init \
      bash \
      ca-certificates \
      protobuf \
      curl \
    " \
    # PACKAGES needed to built python
    PYTHON_BUILD_PACKAGES="\
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

RUN  \
    apk add --no-cache --virtual=.build-dependencies wget ca-certificates && \
    echo \
        "-----BEGIN PUBLIC KEY-----\
        MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApZ2u1KJKUu/fW4A25y9m\
        y70AGEa/J3Wi5ibNVGNn1gT1r0VfgeWd0pUybS4UmcHdiNzxJPgoWQhV2SSW1JYu\
        tOqKZF5QSN6X937PTUpNBjUvLtTQ1ve1fp39uf/lEXPpFpOPL88LKnDBgbh7wkCp\
        m2KzLVGChf83MS0ShL6G9EQIAUxLm99VpgRjwqTQ/KfzGtpke1wqws4au0Ab4qPY\
        KXvMLSPLUp7cfulWvhmZSegr5AdhNw5KNizPqCJT8ZrGvgHypXyiFvvAH5YRtSsc\
        Zvo9GI2e2MaZyo9/lvb+LbLEJZKEQckqRj4P26gmASrZEPStwc+yqy1ShHLA0j6m\
        1QIDAQAB\
        -----END PUBLIC KEY-----" | sed 's/   */\n/g' > "/etc/apk/keys/sgerrand.rsa.pub" && \
    wget \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BASE_URL/$ALPINE_GLIBC_PACKAGE_VERSION/$ALPINE_GLIBC_I18N_PACKAGE_FILENAME" && \
    apk add --no-cache \
        "$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_I18N_PACKAGE_FILENAME" && \
    \
    rm "/etc/apk/keys/sgerrand.rsa.pub" && \
    /usr/glibc-compat/bin/localedef --force --inputfile POSIX --charmap UTF-8 "$LANG" || true && \
    echo "export LANG=$LANG" > /etc/profile.d/locale.sh && \
    \
    apk del glibc-i18n && \
    \
    rm "/root/.wget-hsts" && \
    apk del .build-dependencies && \
    rm \
        "$ALPINE_GLIBC_BASE_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_BIN_PACKAGE_FILENAME" \
        "$ALPINE_GLIBC_I18N_PACKAGE_FILENAME"

RUN set -ex ;\
    # find MAJOR and MINOR python versions based on $PYTHON_VERSION
    export PYTHON_MAJOR_VERSION=$(echo "${PYTHON_VERSION}" | rev | cut -d"." -f3-  | rev) ;\
    export PYTHON_MINOR_VERSION=$(echo "${PYTHON_VERSION}" | rev | cut -d"." -f2-  | rev) ;\
    # replacing default repositories with edge ones
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/community" >> /etc/apk/repositories ;\
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/main" >> /etc/apk/repositories ;\
    # Add the packages, with a CDN-breakage fallback if needed
    apk add --no-cache $PACKAGES || \
        (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache $PACKAGES) ;\
    # Add packages just for the python build process with a CDN-breakage fallback if needed
    apk add --no-cache --virtual .build-deps $PYTHON_BUILD_PACKAGES || \
        (sed -i -e 's/dl-cdn/dl-4/g' /etc/apk/repositories && apk add --no-cache --virtual .build-deps $PYTHON_BUILD_PACKAGES) ;\
    # turn back the clock -- so hacky!
    echo "http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/main/" > /etc/apk/repositories ;\
    # echo "@community http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/community" >> /etc/apk/repositories ;\
    # echo "@testing http://dl-cdn.alpinelinux.org/alpine/v$ALPINE_VERSION/testing" >> /etc/apk/repositories ;\
    # echo "@edge-main http://dl-cdn.alpinelinux.org/alpine/edge/main" >> /etc/apk/repositories ;\
    # use pyenv to download and compile specific python version
    git clone --depth 1 https://github.com/pyenv/pyenv /usr/local/lib/pyenv ;\
    # install
    GNU_ARCH="$(dpkg-architecture --query DEB_BUILD_GNU_TYPE)" ;\
    PYENV_ROOT=/usr/local/lib/pyenv CONFIGURE_OPTS="--build=$GNU_ARCH --enable-loadable-sqlite-extensions --enable-shared --with-system-expat --with-system-ffi --without-ensurepip --with-shared" /usr/local/lib/pyenv/bin/pyenv install $PYTHON_VERSION ;\
    # keep the needed .so files
    # ignore libpython - that one comes from the pyenv instalation
    find /usr/local -type f -executable -not \( -name '*tkinter*' \) -exec scanelf --needed --nobanner --format '%n#p' '{}' ';' \
        | tr ',' '\n' \
        | sort -u \
        | awk 'system("[ -e /usr/local/lib/" $1 " ]") == 0 { next } { print "so:" $1 }' \
        | grep -ve 'libpython' \
        | xargs -rt apk add --no-cache --virtual .python-rundeps ;\
        # for debug
        # | xargs -n1 echo ;\
    # delete everything from pyenv except the installed version
    # this throws an error but we ignore it
    find /usr/local/lib/pyenv/ -mindepth 1 -name versions -prune -o -exec rm -rf {} \; || true ;\
    # delete files to to reduce container size
    # tips taken from main python docker repo
    find /usr/local/lib/pyenv/versions/$PYTHON_VERSION/ -depth \( -name '*.pyo' -o -name '*.pyc' -o -name 'test' -o -name 'tests' \) -exec rm -rf '{}' + ;\
    # symlink the binaries
    ln -s /usr/local/lib/pyenv/versions/$PYTHON_VERSION/bin/* $PYTHON_PATH
    # remove build dependencies and any leftover apk cache
RUN pip3 install --no-cache-dir cryptography protobuf requests ;\
    apk del --no-cache --purge .build-deps ;\
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/usr/bin/dumb-init", "bash", "-l", "-c"]