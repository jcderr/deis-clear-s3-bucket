FROM ubuntu:14.04
MAINTAINER Jeremy Derr <jcderr@radius.com>

RUN apt-get -qq update; apt-get install -yq python python-pip; pip install s3cmd; pip install boto

ADD deleter.py /usr/bin/deleter.py

EXPOSE 8080

CMD python /usr/bin/deleter.py
