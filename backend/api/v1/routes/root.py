from fastapi import APIRouter, Depends

from ...core.config import Settings, get_settings

router = APIRouter()


@router.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name, "description": settings.description}
