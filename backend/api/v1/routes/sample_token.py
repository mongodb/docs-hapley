from fastapi import APIRouter

from ...core.middleware.authorization import Authorization

router = APIRouter()


@router.get(
    "/sample-token",
    tags=["local-development"],
    description="Generate a sample JWT to add to `.env` in local development",
)
async def generate_sample_token(email: str, username: str):
    return {"token": Authorization.build_sample_token(email, username)}
