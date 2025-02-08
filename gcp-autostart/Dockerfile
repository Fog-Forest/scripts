FROM python:3.9-alpine
LABEL authors="Kinoko"

WORKDIR /app
COPY ./app/* .

# 安装依赖
RUN apk update \
    && apk add --no-cache build-base g++ linux-headers \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-base linux-headers

CMD ["python", "main.py"]
