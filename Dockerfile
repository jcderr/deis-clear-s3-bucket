FROM ubuntu:14.04
MAINTAINER Jeremy Derr <jcderr@radius.com>

RUN apt-get -qq update; apt-get install -yq python python-pip; pip install s3cmd

