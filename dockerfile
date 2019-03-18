FROM python:3.6-slim

LABEL maintainer="Mr-Linus admin@geekfan.club"

ARG TZ="Asia/Shanghai"

ENV TZ ${TZ}

ARG  PROJECT_NAME="image-pull"

ENV PROJECT_NAME ${PROJECT_NAME}

COPY . /${PROJECT_NAME}

RUN mv /${PROJECT_NAME}/settings-example.py /${PROJECT_NAME}/settings.py \
    && pip install -r /${PROJECT_NAME}/requirements.txt


ENTRYPOINT ["python", "/image-pull/pull.py" "-s", "mirrors.geekcloud.top","-f", "/image-pull/image.txt","-i"]
CMD[" "]