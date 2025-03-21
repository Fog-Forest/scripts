from typing import Optional, Dict

from pydantic import BaseModel


class RequestData(BaseModel):
    """
    API请求参数结构体

    Attributes:
        method: HTTP请求方法
        url: 目标请求地址
        header: 自定义请求头（可选）
        data: 请求携带的数据（可选）
        maxTimeout: 最大超时时间（毫秒）
        proxy: 代理服务器配置（可选）
    """
    method: str
    url: str
    header: Optional[Dict] = {}
    data: Optional[str] = ""
    maxTimeout: Optional[int] = 60000
    proxy: Optional[Dict[str, str]] = None
