FROM python:3.10-slim

RUN apt-get update && apt-get upgrade -y

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG USER_NAME=appuser
ARG USER_UID=0
ARG USER_GID=0

RUN apt-get update \
    && apt-get install -y sudo \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /etc/sudoers.d/

USER $USER_NAME

WORKDIR /home/$USER_NAME
COPY . /home/$USER_NAME

USER root

RUN sudo rm /var/lib/dpkg/lock-frontend && sudo apt-get update

RUN apt-get update && apt-get install -y \
    gcc \
    wget \
    tar \
    sed \
    git \
    xz-utils \
    g++ \
    make \
    build-essential \
    curl \
    llvm \
    cmake \
    nano \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip & python3 -m pip install --upgrade setuptools
RUN python3 -m pip install -r requirements.txt

RUN cd mn-bab-verification && sudo sh setup.sh
CMD ["/bin/bash"]