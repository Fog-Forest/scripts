from app.config import settings
from app.models.schema import RequestData
from app.services import browser
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/v1", tags=["API"])  # 配置路由前缀和标签


@router.post("/request")
async def api_request(request_data: RequestData):
    try:
        return await browser.handle_browser_request(request_data)
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 健康检查
@router.get("/health", include_in_schema=False)
async def health_check():
    return {"status": "ok", "version": settings.APP_VERSION}
