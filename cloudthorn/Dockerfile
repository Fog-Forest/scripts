FROM python:3.9-alpine

# 设置标签和变量
LABEL authors="Kinoko"
ARG TARGETARCH

# 设置工作目录
COPY ./app /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium && \
    playwright install-deps


ENTRYPOINT ["python", "mian.py"]

# 设置用户为 root
USER root
