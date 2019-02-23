FROM python:3.6-jessie

LABEL maintainer="Mr-Linus admin@geekfan.club"

ARG TZ="Asia/Shanghai"

ENV TZ ${TZ}

ARG  PROJECT_NAME="image-pull"

ENV PROJECT_NAME ${PROJECT_NAME}

COPY . /${PROJECT_NAME}

RUN mv /${PROJECT_NAME}/settings-example.py /${PROJECT_NAME}/settings.py \
    && pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r /${PROJECT_NAME}/requirements.txt


CMD [ "python", "/image-pull/pull.py", "-f", "/image-pull/image-k8s.txt" ]