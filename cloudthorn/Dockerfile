FROM python:3.10-slim

# 设置标签和变量
LABEL authors="Kinoko"

# 设置工作目录
COPY ./app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium \
    && playwright install-deps


ENTRYPOINT ["python", "main.py"]

# 设置用户为 root
USER root
