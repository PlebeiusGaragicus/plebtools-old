FROM python:3.11.0-alpine
# FROM python:3.11.0-alpine3.16
# FROM python:3.8.3-alpine
# FROM python:3.8.3
# FROM python:slim-buster

# https://www.cyberciti.biz/faq/alpine-linux-install-bash-using-apk-command/
# adds about 4MB to the image
# WE DON'T NEED THESE ANYMORE BECAUSE WE'RE USING PYTHON:3.11.0-ALPINE AND PYTHON IS THE SHIT
# RUN apk update
# RUN apk add curl jq

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# COPY .env .env
COPY /web /web
COPY /src /src
COPY /data /data
RUN chmod -R 777 /data



ADD ./docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh
RUN chmod a+x /usr/local/bin/docker_entrypoint.sh

# TODO - this prevents the app from being able to save settings.json
# I need to look into this
USER 1000

# TODO does this matter?  Can I just use the default.. like 5000?
EXPOSE 8080
