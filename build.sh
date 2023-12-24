#!/usr/bin/env bash

docker build \
       -t resource-monitor:0.0.1 \
       . \
       --platform="linux/amd64"

docker tag resource-monitor:0.0.1 resource-monitor:latest
