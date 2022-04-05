# syntax=docker/dockerfile:1
FROM python:3.9-alpine
COPY . /server
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip install -r /server/requirements.txt
CMD python3 /server/server.py
