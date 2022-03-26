FROM nginx
LABEL org.opencontainers.image.authors="Kinoko"

RUN apt update \
    && apt install cron -y \
    && curl  https://get.acme.sh | sh -s email=admin@zmkan.top \
    && ln -s /root/.acme.sh/acme.sh /usr/bin/acme.sh \
    && chmod +x /usr/bin/acme.sh \
    && acme.sh  --upgrade  --auto-upgrade

EXPOSE 80 443
USER root