FROM debian:stretch-slim

WORKDIR /

COPY fast-pull /usr/local/bin

CMD ["fast-pull","get","-f","/root/image.txt"]