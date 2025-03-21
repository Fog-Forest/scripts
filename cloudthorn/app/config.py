from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_CONFIG = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
    "viewport": {"width": 1920, "height": 1080},
    "browser_args": [
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox'
    ],
    "max_timeout": 30000  # 浏览器启动超时
}


class Settings(BaseSettings):
    # 应用基础配置
    APP_NAME: str = "Cloudthorn"
    APP_DESCRIPTION: str = "绕过 Cloudflare 的无头浏览器API服务"
    APP_VERSION: str = "1.0"
    DEBUG: bool = False

    # 服务端配置
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8675
    UVICORN_WORKERS: int = 1

    # 配置加载规则（环境变量优先，其次.env文件）
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
