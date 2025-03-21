from app.config import DEFAULT_CONFIG
from app.models.schema import RequestData
from app.utils import simulator, proxy
from fastapi import HTTPException
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async


async def handle_browser_request(params: RequestData):
    """浏览器请求处理主入口"""
    async with async_playwright() as p:
        # 配置浏览器启动参数
        launch_options = {
            "headless": True,  # 无头模式开关
            "args": DEFAULT_CONFIG["browser_args"],  # 启动参数如禁用沙箱等
            "timeout": DEFAULT_CONFIG["max_timeout"]  # 全局超时设置
        }

        # 代理配置处理
        proxy_config = proxy.parse_proxy(params.proxy or {})
        if proxy_config:
            launch_options["proxy"] = proxy_config

        try:
            # 浏览器实例初始化
            browser = await p.chromium.launch(**launch_options)
            # 创建新上下文隔离会话
            context = await browser.new_context(
                user_agent=DEFAULT_CONFIG["user_agent"],  # 默认UA
                viewport=DEFAULT_CONFIG["viewport"]  # 默认视口尺寸
            )
            page = await context.new_page()  # 创建新标签页

            # 反检测措施
            await stealth_async(page)  # 应用playwright-stealth的伪装
            # 移除webdriver特征
            await page.add_init_script("""
                delete navigator.__proto__.webdriver;
            """)

            # 请求头处理
            if params.header:  # 自定义请求头覆盖默认设置
                await page.set_extra_http_headers(params.header)

            # 执行请求逻辑
            result = await _process_request(page, params)
            return result

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        finally:
            if 'browser' in locals():  # 确保浏览器实例被清理
                await browser.close()


async def _process_request(page, params: RequestData):
    method = params.method.lower()  # 统一小写处理

    # GET请求处理流程
    if method == "get":
        # 导航到目标页面并等待网络空闲
        response = await page.goto(
            params.url,
            timeout=params.maxTimeout,  # 页面加载超时
            wait_until="networkidle"  # 等待网络活动停止
        )
        await simulator.human_like_actions(page)  # 模拟人类操作
        content = await page.content()  # 获取完整HTML内容

    # POST请求处理流程
    elif method == "post":
        # 直接发起API请求（不加载页面）
        response = await page.request.post(
            params.url,
            headers=params.header,  # 透传自定义请求头
            data=params.data,  # POST数据体
            timeout=params.maxTimeout  # 请求超时设置
        )
        content = await response.text()  # 获取响应文本

    else:
        raise HTTPException(status_code=400, detail="Method not supported")

    # 统一响应格式
    return {
        "status": "success",
        "data": {
            "content": content,  # 网页内容
            "headers": dict(response.headers),
            "status_code": response.status  # HTTP状态码
        }
    }
