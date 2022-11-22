FROM python:3.11.0-alpine
# FROM python:3.11.0-alpine3.16
# FROM python:3.8.3-alpine
# FROM python:3.8.3
# FROM python:slim-buster

# RUN apt-get update
# RUN apt-get install -y python3 python3-pip

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# COPY .env .env
COPY /data /data
COPY /src /app



ADD ./docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh
RUN chmod a+x /usr/local/bin/docker_entrypoint.sh

USER 1000

# TODO does this matter?  Can I just use the default.. like 5000?
EXPOSE 8069

# CMD [ "python", "-m", "this_app" ]
# ENTRYPOINT [ "python", "-m", "app" ]


# IMAGE SOURCE
# https://hub.docker.com/layers/library/debian/buster-slim/images/sha256-f567c8d4f1fed214cfec2dbc5c55bef619d9053ef6ce3f08659bb8e2b744ed8c?context=explore
# ADD file:14c4aa7a...
# https://hub.docker.com/layers/library/python/slim-buster/images/sha256-09b30e3221996c42d14b05ee6bbc7a38e9a81d805748b43d50ce19a597ecabd3?context=explore
# ADD file:14c4aa7a...

# MULTI-STAGE BUILD
# https://docs.docker.com/build/building/multi-stage/
# TODO
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
# https://www.nannyml.com/blog/three-things-i-learned-whilst-containerizing-a-python-api
