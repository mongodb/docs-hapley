from os import getenv
from time import time

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware

from ..util.jwt import TokenData, parse_jwt


class UnauthorizedOktaGroup(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not authorized to access this resource.",
        )

    def __str__(self):
        return self.detail


# Implement custom middleware by overriding BaseHTTPMiddleware.dispatch
class Authorization(BaseHTTPMiddleware):

    AUTHORIZED_OKTA_GROUPS: set = set(["10gen-docs-platform"])
    SAMPLE_TOKEN_PATH = "/api/v1/sample-token"

    async def dispatch(self, request: Request, call_next):
        # Allow sample token requests to proceed without authorization
        if request.url.path == self.SAMPLE_TOKEN_PATH:
            return await call_next(request)

        try:
            # For local development, JWT comes from env file not Authorization header
            auth_headers = request.headers.get("Authorization")
            token = (auth_headers and self.parse_header(auth_headers)) or getenv(
                "JWT_TOKEN"
            )
            token_data: TokenData = parse_jwt(token)

            if bool(self.AUTHORIZED_OKTA_GROUPS & set(token_data.groups)):
                request.state.user = token_data
                response = await call_next(request)
            else:
                raise UnauthorizedOktaGroup()
        except (UnauthorizedOktaGroup, JWTError) as e:
            context = (
                "See README for instructions on creating a JWT token if developing locally"
                if e.__class__ == JWTError
                else "Ensure you are a member of an authorized Okta group"
            )
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "message": f"Unauthorized. Error message: {e} {context}",
                },
            )
        return response

    def parse_header(self, auth_headers: str):
        return auth_headers.split(" ")[1]

    @classmethod
    def build_sample_token(
        cls, email: str, username: str, is_authorized: bool = True
    ) -> str:
        SECONDS_PER_WEEK = 60 * 60 * 24 * 7
        groups = list(cls.AUTHORIZED_OKTA_GROUPS) if is_authorized else []
        future_timestamp: int = int(time() + SECONDS_PER_WEEK)
        to_encode: dict = {
            "email": email,
            "sub": username,
            "groups": groups,
            "exp": future_timestamp,
        }
        return jwt.encode(to_encode, "secret")
