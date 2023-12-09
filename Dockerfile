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

#RUN groupadd --gid $USER_GID $USER_NAME \
#    && useradd --uid $USER_UID --gid $USER_GID --create-home --shell /bin/bash $USER_NAME

RUN mkdir -p /etc/sudoers.d/

# Add the user to the sudo group and grant sudo privileges
#RUN usermod -aG sudo $USER_NAME \
#    && echo "$USER_NAME ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/$USER_NAME

#RUN chown -R $USER_NAME:$USER_NAME /var/lib/apt/lists

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

#USER $USER_NAME
# Install pip requirements
COPY requirements.txt .
RUN python3 -m pip install --upgrade pip & python3 -m pip install --upgrade setuptools
RUN python3 -m pip install -r requirements.txt

RUN cd mn-bab-verification && sudo sh setup.sh
CMD ["/bin/bash"]