# EarnAPP 平台设备注册API

### 说明

EarnAPP 平台设备不能自动注册，还得用手动用链接添加，于是抓包获取到了注册设备的接口，二次封装了一个 API

### 部署

```bash
# 运行
# Token 登陆官网 `F12` 从 Cookie 中即可获得
docker run -d \
  -p 5000:5000 \
  --name earnapp-api \
  --restart=always \
  -e PORT=5000 \
  -e XSRF_TOKEN="your_token" \
  -e OAUTH_REFRESH_TOKEN="your_token" \
  fogforest/earnapp-api
```

```bash
# 请求
curl -X POST http://127.0.0.1:5000/api/get_result -H "Content-Type: application/json" -d '{"uuid": "sdk-node-7a3b43f516a3490d8ba4c3d459bb34b1"}'
```
