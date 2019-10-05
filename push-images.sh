#!/usr/bin/env bash

echo "Build Images..."
sudo docker build -t registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:latest .
echo "Push Images..."
sudo docker push registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:latest