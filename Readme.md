## image-pull
基于 GRPC/Python3 开发，用于拉取 k8s.gcr.io、 quay.io等境外仓库中的镜像工具。


### 用法
拉取镜像：quay.io/coreos/flannel:v0.11.0
```python
python3 pull.py \
        -i quay.io/coreos/flannel:v0.11.0 \ 
        -s mirrors.geekcloud.top
```

### 境外服务器节点部署
- 配置
重命名`settings-example.py`文件为`settings.py`，并设置相关参数
```bash
# 仓库地址
RepoUrl = "registry.cn-hangzhou.aliyuncs.com"
# 仓库命名空间
RepoNamespace = "sp"
# 以下为阿里云镜像仓库配置参数：
# 产品名
Product_name = "cr"
# 镜像仓库所在位置
Region_id = "cn-hangzhou"
# 镜像仓库节点名
End_point = "cr.cn-hangzhou.aliyuncs.com"
# 阿里云镜像仓库 RAM 用户ID
id = "123"
# 阿里云镜像仓库 RAM 用户key
key = "666"
# 阿里云镜像仓库 RAM 用户名
username = "admin"
# 阿里云镜像仓库 RAM 密码
password = "123"
# 境外服务器工作端口
server_listen = '[::]:50051'
# 境外服务器域名或地址
host= "www.example.com"
```
- 安装依赖与部署
```shell
pip3 install -r requirements.txt
python3 server.py
```
