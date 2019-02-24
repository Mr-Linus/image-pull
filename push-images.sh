#!/usr/bin/env bash

echo "Build Images..."
sudo docker login -u $username -p $password registry.cn-hangzhou.aliyuncs.com
sudo docker build -t registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:k8s-1.13.3 .
echo "Push Images..."
sudo docker push registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:k8s-1.13.3
sudo docker logout