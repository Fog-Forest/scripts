# debug.py
import asyncio

from playwright.async_api import async_playwright

from app.models.schema import RequestData
from app.services.browser import handle_browser_request


async def debug_browser():
    # 测试参数配置
    test_params = RequestData(
        method="get",
        url="https://api.akile.io/",  # 浏览器指纹测试网站
        header={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:136.0) Gecko/20100101 Firefox/136.0"
        },
        proxy={},
        maxTimeout=30000
    )

    # 覆盖配置为调试模式
    test_params.proxy = None  # 注释掉这行使用代理
    debug_config = {
        "headless": False,
        "devtools": True,  # 打开开发者工具
        "slow_mo": 500,  # 放慢操作速度（毫秒）
        "args": [
            '--window-size=1280,720'
        ]
    }

    async with async_playwright() as p:
        print("🚀 启动浏览器...")
        browser = await p.chromium.launch(**debug_config)

        try:
            print("🔎 正在访问目标网站...")
            result = await handle_browser_request(test_params)
            print("✅ 请求成功！")
            print(f"状态码: {result['data']['status_code']}")
            print(result["data"]["content"])

            # 保持浏览器打开用于检查
            print("🕒 进入调试模式（60秒后自动关闭）...")
            await asyncio.sleep(60)

        except Exception as e:
            print(f"❌ 发生错误: {str(e)}")
        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(debug_browser())
