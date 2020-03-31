FROM python:3.6-slim

ARG TZ="Asia/Shanghai"

ENV TZ ${TZ}

ARG  PROJECT_NAME="image-pull"

ENV PROJECT_NAME ${PROJECT_NAME}

WORKDIR  ${PROJECT_NAME}

COPY . /${PROJECT_NAME}

RUN  pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  -r /${PROJECT_NAME}/requirements.txt


ENTRYPOINT ["python", "server.py"]

#ENTRYPOINT ["python", "/image-pull/pull.py","-s", "azure.geekcloud.top","-f", "/image-pull/image.txt","-i"]

#CMD [" "]