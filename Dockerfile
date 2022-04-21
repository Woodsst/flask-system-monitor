# syntax=docker/dockerfile:1
FROM python:3.9-alpine
COPY . flask_system_monitor
RUN apk add --update gcc libc-dev linux-headers && rm -rf /var/cache/apk/*
RUN pip install -r flask_system_monitor/server/requirements.txt
CMD python3 flask_system_monitor/server/server.py
