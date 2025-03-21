# Cloudthorn
基于 FastAPI 的 API 服务，用于通过无头浏览器绕过 Cloudflare 检测。可以理解为 Flaresolverr 加强版，因为 Flaresolverr 不支持自定义 Header，本项目 80% 代码由 DeepSeek 生成。

## 快速开始

### 配置管理

## API 文档

1. 发送请求
端点: `POST /api/request`
功能: 代理请求到目标 URL
请求示例:
```json
{
  "method": "GET",
  "url": "https://www.baidu.com/",
  "header": {"User-Agent": "Custom Agent"},
  "maxTimeout": 30000
}
```
```json
{
  "method": "POST",
  "url": "https://www.baidu.com/",
  "header": {"User-Agent": "Custom Agent"},
  "data": "",
  "maxTimeout": 30000
}
```
响应示例 (成功):
```json
{
  "content": "<html>...</html>",
  "status_code": 200
}
```

2. 健康检查
端点: GET /health
响应:
```json
{"status": "ok"}
```
