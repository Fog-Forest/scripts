FROM python:3.7

MAINTAINER kinoko <admin@amogu.cn>

ADD ./code /code
WORKDIR /code

# 安装运行库
RUN pip install -r requirements.txt \
    && pip list
CMD [ "python","main.py" ]
ENV TZ=Asia/Shanghai
USER root
