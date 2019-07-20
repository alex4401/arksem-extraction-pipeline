FROM archlinux/base

RUN pacman -Sy --noconfirm unzip python protobuf \
                           python-cryptography python-protobuf \
                           python-requests &&\
    pacman -Scc --noconfirm