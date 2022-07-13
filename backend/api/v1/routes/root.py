from fastapi import APIRouter
from ...core.config import get_settings

router = APIRouter()


@router.get("/")
async def root():
    settings = get_settings()
    return {"app_name": settings.app_name}
