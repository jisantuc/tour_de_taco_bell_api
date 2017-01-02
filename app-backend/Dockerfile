FROM python:3.6
ENV PYTHONBUFFERED 1

RUN apt-get update
RUN apt-get install -y python-dev

RUN mkdir /ttb-core
WORKDIR /ttb-core
ADD ./requirements.txt /ttb-core
RUN pip install -r requirements.txt
ADD . /ttb-core

RUN django-admin.py startproject ttbcore