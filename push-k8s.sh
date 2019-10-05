#!/usr/bin/env bash
sudo kubeadm config images list 2> /dev/null 1> image.txt
echo "Pulling K8S Images"
sudo docker run --rm -it \
        -v $(pwd)/image.txt:/image-pull/image.txt \
        -v /var/run/docker.sock:/var/run/docker.sock  \
        registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:latest
version=$(kubeadm config images list | head -1 | awk -F: '{ print $2 }')
echo "Deploy the latest version: $version"
echo "Build Images $version..."
sudo docker build -t registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:k8s-$version .
echo "Push Images $version..."
sudo docker push registry.cn-hangzhou.aliyuncs.com/geekcloud/image-pull:k8s-$version
sudo docker logout
