#!/bin/sh

# first run
# if [ ! -f /root/passwd ]; then
#     password=$(cat /dev/urandom | base64 | head -c 16)
#     echo "$password" >> /root/passwd
# fi

# REMEMBER:
# stats = properties
# config = config

# https://github.com/Start9Labs/filebrowser-wrapper/blob/master/docker_entrypoint.sh#L15-L30
write_properties_stats_yaml() {
    mkdir -p /root/start9
    password=$(cat /dev/urandom | base64 | head -c 16)
    echo 'data:' >> /root/start9/stats.yaml
    echo '  Default Username:' >> /root/start9/stats.yaml
    echo '    type: string' >> /root/start9/stats.yaml
    echo '    value: admin' >> /root/start9/stats.yaml
    echo '    description: This is your default username. While it is not necessary, you may change it inside your File Browser web application. That change, however, will not be reflected here. If you change your default username and forget your new username, you can regain access by resetting the root user.' >> /root/start9/stats.yaml
    echo '    copyable: true' >> /root/start9/stats.yaml
    echo '    masked: false' >> /root/start9/stats.yaml
    echo '    qr: false' >> /root/start9/stats.yaml
    echo '  Default Password:' >> /root/start9/stats.yaml
    echo '    type: string' >> /root/start9/stats.yaml
    echo '    value: "'"$password"'"' >> /root/start9/stats.yaml
    echo '    description: This is your randomly-generated, default password. While it is not necessary, you may change it inside your File Browser web application. That change, however, will not be reflected here.' >> /root/start9/stats.yaml
    echo '    copyable: true' >> /root/start9/stats.yaml
    echo '    masked: true' >> /root/start9/stats.yaml
    echo '    qr: false' >> /root/start9/stats.yaml
}

write_properties_stats_yaml()

# https://github.com/Start9Labs/filebrowser-wrapper/blob/master/health-check.sh
# TODO ... I don't get this...
# health-check.sh &


# run the application
exec python -m src
# https://github.com/goshiz/start9labs-havend-wrapper/blob/master/docker_entrypoint.sh
# exec /usr/bin/local python3 -m src
