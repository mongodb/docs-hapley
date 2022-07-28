from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...core.config import Settings, get_settings

router = APIRouter()


class ApiDescription(BaseModel):
    app_name: str
    description: str


@router.get("/", response_model=ApiDescription, tags=["default"])
async def root(settings: Settings = Depends(get_settings)):
    return {"app_name": settings.app_name, "description": settings.description}
