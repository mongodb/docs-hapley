from fastapi import APIRouter
from ...core.middleware.authorization import Authorization

router = APIRouter()


@router.get("/sample-token")
async def generate_sample_token(email: str, username: str):
    return {"token": Authorization.build_sample_token(email, username)}
