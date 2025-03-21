import uvicorn
from app.config import settings
from app.routers import api
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
        # 文档安全三连关闭
        docs_url=None,  # 禁用Swagger UI (/docs)
        redoc_url=None,  # 禁用ReDoc (/redoc)
        openapi_url=None  # 禁用OpenAPI规范 (/openapi.json)
    )

    # 添加中间件
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 注册路由
    app.include_router(api.router)

    return app


app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=False,
        workers=settings.UVICORN_WORKERS,
        timeout_keep_alive=30
    )
