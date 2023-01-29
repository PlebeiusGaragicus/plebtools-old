FROM python:3.11.0-alpine


# PYTHON REQUIREMENTS
COPY requirements.txt .
RUN apk update
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt


# SHELL SCRIPTS
ADD ./docker_entrypoint.sh /usr/local/bin/docker_entrypoint.sh
# RUN chmod a+x /usr/local/bin/docker_entrypoint.sh

COPY ./actions /usr/local/bin
# ADD ./actions/delete-debug-log.sh /usr/local/bin/delete-debug-log.sh
RUN chmod a+x /usr/local/bin/*.sh


# THE PYTHON APPLICATION
WORKDIR /root

COPY /web /web
COPY /src /src
COPY /data /data
RUN chmod -R 777 /data

# do not run as root, use a user with limited permissions instead
USER 1000

EXPOSE 8080

ENTRYPOINT ["/usr/local/bin/docker_entrypoint.sh"]
