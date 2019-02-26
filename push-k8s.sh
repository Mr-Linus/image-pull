#!/usr/bin/env bash
swapoff -a
sudo curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install kubeadm
kubeadm config images list > image.txt
docker run --rm -it \
        -v $(pwd)/image.txt:/image-pull/image.txt \
        -v /var/run/docker.sock:/var/run/docker.sock  \
        registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:latest