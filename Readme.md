## image-pull
基于GRPC用于推拉 k8s.gcr.io 与 quay.io仓库的镜像工具。


### Usage
拉取镜像：quay.io/coreos/flannel:v0.11.0
```python
python3 pull.py \
        -i quay.io/coreos/flannel:v0.11.0 \ 
        -s mirrors.geekcloud.top
```
