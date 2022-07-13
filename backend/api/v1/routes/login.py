from fastapi import APIRouter
from ...core.middleware.authorization import Authorization

router = APIRouter()


@router.get("/login")
async def login(email: str, username: str):
    return {"token": Authorization.build_sample_token(email, username)}
