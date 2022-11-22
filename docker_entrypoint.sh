#!/bin/sh

# first run
if [ ! -f /root/passwd ]; then
    password=$(cat /dev/urandom | base64 | head -c 16)
    echo "$password" >> /root/passwd
fi

# https://github.com/Start9Labs/filebrowser-wrapper/blob/master/docker_entrypoint.sh#L15-L30
write_properties_stats_yaml() {
    echo 'version: 2' > /root/start9/stats.yaml
    echo 'data:' >> /root/start9/stats.yaml
    echo '  Hello:' >> /root/start9/stats.yaml
    echo '    type: string' >> /root/start9/stats.yaml
    echo '    value: admin' >> /root/start9/stats.yaml
    echo '    description: This is .' >> /root/start9/stats.yaml
    echo '    copyable: true' >> /root/start9/stats.yaml
    echo '    masked: false' >> /root/start9/stats.yaml
    echo '    qr: false' >> /root/start9/stats.yaml
    echo '  World:' >> /root/start9/stats.yaml
    echo '    type: string' >> /root/start9/stats.yaml
    echo '    value: "'"$password"'"' >> /root/start9/stats.yaml
    echo '    description: This randomly-generated.' >> /root/start9/stats.yaml
    echo '    copyable: true' >> /root/start9/stats.yaml
    echo '    masked: true' >> /root/start9/stats.yaml
    echo '    qr: false' >> /root/start9/stats.yaml
}


# health-check.sh &

# run the application
python -m src
