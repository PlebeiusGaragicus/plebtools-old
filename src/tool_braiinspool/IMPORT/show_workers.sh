#!/bin/bash -i

# change the directory to the one that this current running script is in (so relative pathnames work) - this is so "crontab -e" works...
cd $(dirname "$0")

. ./braiins_api.sh

ret=$(callSlushAPI $URLworkers)
echo $ret | jq '.btc.workers'
