#!/usr/bin/env bash
sudo swapoff -a
echo "Update System.."
sudo apt-get update && sudo apt-get install -y apt-transport-https curl
echo "Install kubeadm.."
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl
sudo kubeadm config images list > image.txt
sudo docker run --rm -it \
        -v $(pwd)/image.txt:/image-pull/image.txt \
        -v /var/run/docker.sock:/var/run/docker.sock  \
        registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:latest