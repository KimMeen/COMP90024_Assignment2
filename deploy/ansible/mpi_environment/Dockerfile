FROM ubuntu:16.04

# TensorFlow version is tightly coupled to CUDA and cuDNN so it should be selected carefully
ENV TENSORFLOW_VERSION=1.12.0

# Python 2.7 or 3.5 is supported by Ubuntu Xenial out of the box
ARG python=3.5
ENV PYTHON_VERSION=${python}

RUN apt-get update && apt-get install -y --allow-downgrades --allow-change-held-packages --no-install-recommends \
        build-essential \
        cmake \
        git \
        curl \
        vim \
        wget \
        ca-certificates \
        python${PYTHON_VERSION} \
        python${PYTHON_VERSION}-dev

RUN ln -s /usr/bin/python${PYTHON_VERSION} /usr/bin/python

RUN curl -O https://bootstrap.pypa.io/get-pip.py && \
    python get-pip.py && \
    rm get-pip.py

# Install TensorFlow, Keras, nltk
RUN pip install 'numpy<1.15.0' tensorflow==${TENSORFLOW_VERSION} keras h5py nltk 

# Install Open MPI
RUN mkdir /tmp/openmpi && \
    cd /tmp/openmpi && \
    wget https://www.open-mpi.org/software/ompi/v4.0/downloads/openmpi-4.0.0.tar.gz && \
    tar zxf openmpi-4.0.0.tar.gz && \
    cd openmpi-4.0.0 && \
    ./configure --enable-orterun-prefix-by-default && \
    make -j $(nproc) all && \
    make install && \
    ldconfig && \
    rm -rf /tmp/openmpi

# Install OpenSSH for MPI to communicate between containers
RUN apt-get install -y --no-install-recommends openssh-client openssh-server && \
    mkdir -p /var/run/sshd

# Allow OpenSSH to talk to containers without asking for confirmation
RUN cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new && \
    echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new && \
    mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config

# Config SSH Demon only allow authorized hosts
RUN cat /etc/ssh/sshd_config | grep -v Port > /etc/ssh/sshd_config.new && \
    echo "Port 1234" >> /etc/ssh/sshd_config.new && \
    mv /etc/ssh/sshd_config.new /etc/ssh/sshd_config
RUN cat /etc/ssh/sshd_config | grep -v PermitRootLogin > /etc/ssh/sshd_config.new && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config.new && \
    mv /etc/ssh/sshd_config.new /etc/ssh/sshd_config

# Ensure all containers share the same public/private key so that they can communcate with each other


RUN mkdir /root/.ssh && \
    touch /root/.ssh/config && \
    touch /root/.ssh/authorized_keys && \
    touch /root/.ssh/private_key.pem

COPY cccAssi2_public /root/.ssh/authorized_keys
COPY cccAssi2_private.pem /root/.ssh/private_key.pem

RUN chmod 0400 /root/.ssh/private_key.pem && \
    echo "IdentityFile /root/.ssh/private_key.pem" >> /root/.ssh/config 


# install mpi4py and couchdb ahocorapy
RUN pip install mpi4py couchdb ahocorapy

WORKDIR "/mnt"

ENTRYPOINT service ssh restart && /bin/bash