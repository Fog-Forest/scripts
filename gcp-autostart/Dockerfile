FROM python:3.9-alpine
LABEL authors="Kinoko"

# 复制应用代码
COPY ./app /app
WORKDIR /app

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行命令
CMD ["python", "main.py"]