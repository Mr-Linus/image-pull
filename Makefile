all: local

local:
	GOOS=linux GOARCH=amd64 go build .

build:
	sudo docker build --no-cache . -t registry.cn-hangzhou.aliyuncs.com/geekcloud/fast-pull

push:
	sudo docker push registry.cn-hangzhou.aliyuncs.com/geekcloud/fast-pull

format:
	sudo gofmt -l -w .
clean:
	sudo rm -f fast-pull