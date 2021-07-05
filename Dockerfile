FROM alpine:latest
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
RUN apk add --no-cache python3 bash openssh-client py3-paramiko py3-pip vim curl tzdata py3-gunicorn libevent-dev
RUN apk add --no-cache -X http://mirrors.aliyun.com/alpine/edge/testing py3-gevent libev
RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

ENTRYPOINT ["bash", "/start.sh"]

RUN mkdir -p /app
COPY anobbs_core /app/anobbs_core
COPY anobbs_http /app/anobbs_http
COPY setup.py /app
COPY app.py /app

RUN pip3 install -e /app

COPY ./start.sh /start.sh
