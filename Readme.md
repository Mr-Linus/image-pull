## image-pull
基于 GRPC/Python 开发，用于拉取 k8s.gcr.io、 quay.io等境外仓库中的镜像工具。


### Usage
拉取镜像：quay.io/coreos/flannel:v0.11.0
```python
python3 pull.py \
        -i quay.io/coreos/flannel:v0.11.0 \ 
        -s mirrors.geekcloud.top
```
