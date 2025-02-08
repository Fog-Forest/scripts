FROM python:3.9-alpine
LABEL authors="Kinoko"

COPY ./app /app
WORKDIR /app

# 更新 apk 源并安装 tzdata，包括其他必要的依赖项
RUN sed -i 's#https\?://dl-cdn.alpinelinux.org/alpine#https://mirrors.tuna.tsinghua.edu.cn/alpine#g' /etc/apk/repositories \
    && apk update \
    && apk add --no-cache tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && pip install --no-cache-dir -r /app/requirements.txt

ENTRYPOINT [ "python", "main.py" ]

# 容器默认运行的端口
EXPOSE 5000
