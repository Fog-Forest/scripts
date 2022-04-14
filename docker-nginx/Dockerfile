FROM --platform=$TARGETPLATFORM nginx:alpine
LABEL org.opencontainers.image.authors="Kinoko"

RUN apk add openssl \
    && curl  https://get.acme.sh | sh -s email=admin@145541.xyz \
    && ln -s /root/.acme.sh/acme.sh /usr/bin/acme.sh \
    && chmod +x /usr/bin/acme.sh \
    && acme.sh --set-default-ca --server letsencrypt \
    && acme.sh --upgrade --auto-upgrade

EXPOSE 80 443
USER root
