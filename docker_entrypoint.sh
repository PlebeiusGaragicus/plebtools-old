#!/bin/sh

# first run
# if [ ! -f /root/passwd ]; then
#     password=$(cat /dev/urandom | base64 | head -c 16)
#     echo "$password" >> /root/passwd
# fi

# https://github.com/Start9Labs/filebrowser-wrapper/blob/master/docker_entrypoint.sh#L15-L30
# write_properties_stats_yaml() {
#     echo ' python location: ' $(which python) >> ./stats.yaml
#     echo 'version: 2' > ./stats.yaml
#     echo 'data:' >> ./stats.yaml
#     echo '  Hello:' >> ./stats.yaml
#     echo '    type: string' >> ./stats.yaml
#     echo '    value: admin' >> ./stats.yaml
#     echo '    description: This is .' >> ./stats.yaml
#     echo '    copyable: true' >> ./stats.yaml
#     echo '    masked: false' >> ./stats.yaml
#     echo '    qr: false' >> ./stats.yaml
#     echo '  World:' >> ./stats.yaml
#     echo '    type: string' >> ./stats.yaml
#     echo '    value: "'"$password"'"' >> ./stats.yaml
#     echo '    description: This randomly-generated.' >> ./stats.yaml
#     echo '    copyable: true' >> ./stats.yaml
#     echo '    masked: true' >> ./stats.yaml
#     echo '    qr: false' >> ./stats.yaml
# }

# write_properties_stats_yaml()

# health-check.sh &

# run the application
exec python -m src

# https://github.com/goshiz/start9labs-havend-wrapper/blob/master/docker_entrypoint.sh
# exec /usr/bin/local python3 -m src

# get ip address of this mac machine
# echo $(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}')
