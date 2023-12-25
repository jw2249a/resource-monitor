#!/usr/bin/env bash
docker run  \
       -it \
       --gpus all \
       -p 5000:8000 \
       --mount type=bind,source=/var/log/sysstat/,target=/var/log/sysstat/,readonly\
       --device /dev/kfd:/dev/kfd \
       --device /dev/dri:/dev/dri \
       resource-monitor
