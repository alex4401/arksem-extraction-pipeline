FROM python:3.5.8-slim-stretch

RUN apt-get update                          &&  \
    apt-get install -y --no-install-recommends  \
                    python3-cryptography        \
                    protobuf                &&  \
    rm -rf /var/lib/apt/lists/*