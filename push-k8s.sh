#!/usr/bin/env bash
sudo swapoff -a
echo "Update System.."
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
version=v1.14.3
vv=1.14.3-00
echo "Install kubeadm & push images.."
sudo apt-get update
sudo apt-get install -y kubelet=$vv kubeadm=$vv kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo kubeadm config images list > image.txt
sudo docker run --rm -it \
        -v $(pwd)/image.txt:/image-pull/image.txt \
        -v /var/run/docker.sock:/var/run/docker.sock  \
        registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:latest

#version=$(kubeadm config images list | head -1 | awk -F: '{ print $2 }')
echo "Deploy the latest version: $version"
sudo kubeadm config images list > image-k8s.txt
echo "Build Images $version..."
sudo docker login -u $username -p $password registry.cn-hangzhou.aliyuncs.com
sudo docker build -t registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:k8s-$version .
echo "Push Images $version..."
sudo docker push registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:k8s-$version
sudo docker logout
