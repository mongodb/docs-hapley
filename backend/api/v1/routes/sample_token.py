from fastapi import APIRouter
from pydantic import BaseModel
from ...core.middleware.authorization import Authorization

router = APIRouter()


class TokenResponse(BaseModel):
    token: str

@router.get(
    "/sample-token",
    tags=["local-development"],
    response_model=TokenResponse,
    description="Generate a sample JWT to add to `.env` in local development",
)
async def generate_sample_token(email: str, username: str):
    return {"token": Authorization.build_sample_token(email, username)}
