# GCP 抢占式实例自动开机

## 运行容器（需挂载服务账号凭证）

docker run -d --name gcp-autoboot \
-e GCP_PROJECT_ID=your-production-project \
-v /gcp/credentials.json:/app/credentials.json \
fogforest/gcp-autoboot

## 查看日志

docker logs -f gcp-autoboot