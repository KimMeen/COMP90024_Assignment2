FROM ubuntu:16.04

# Python 2.7 or 3.5 is supported by Ubuntu Xenial out of the box
ARG python=3.5
ENV PYTHON_VERSION=${python}

ARG http_proxy="http://wwwproxy.unimelb.edu.au:8000/"
ARG https_proxy="http://wwwproxy.unimelb.edu.au:8000/"

ENV http_proxy $http_proxy
ENV https_proxy $https_proxy

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

# Install TensorFlow, Keras
RUN pip install \
    'numpy<1.15.0' \
    flask \
    shapely \
    couchdb



WORKDIR "/mnt"

