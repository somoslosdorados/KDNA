FROM debian:12.4


USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    git \
    libboost-all-dev \
    libgflags-dev \
    libgoogle-glog-dev \
    libgtest-dev \
    libprotobuf-dev \
    protobuf-compiler \
    python3 \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    wget \
    python3-poetry \
    iputils-ping \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -ms /bin/bash test

USER test
WORKDIR /home/test
# copy the source code to the container
COPY --chown=test:test . .
RUN poetry install --only main

