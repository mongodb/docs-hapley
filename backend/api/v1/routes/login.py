from fastapi import APIRouter
from ...core.middleware.authorization import Authorization
from time import time
from jose import jwt

router = APIRouter()
SECONDS_PER_WEEK = 60 * 60 * 24 * 7


@router.get("/login")
async def login(email: str, username: str):
    future_timestamp: int = int(time() + SECONDS_PER_WEEK)
    to_encode: dict = {
        "email": email,
        "sub": username,
        "groups": list(Authorization.AUTHORIZED_OKTA_GROUPS),
        "exp": future_timestamp,
    }
    token = jwt.encode(to_encode, Authorization.FAKE_JWT_SECRET)
    return {"token": token}
