from fastapi import Request, status, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from ..util.jwt import TokenData, parse_jwt
from jose import JWTError
from os import getenv


# Implement custom middleware by overriding BaseHTTPMiddleware.dispatch
class Authorization(BaseHTTPMiddleware):

    AUTHORIZED_OKTA_GROUPS: set = set(["10gen-docs-platform"])
    FAKE_JWT_SECRET = "secret"
    LOGIN_PATH = "/api/v1/login"

    async def dispatch(self, request: Request, call_next):
        # Allow login requests to proceed without authorization
        if request.url.path == self.LOGIN_PATH:
            return await call_next(request)

        try:
            token = getenv("JWT_TOKEN") or self.parse_header(request)
            token_data: TokenData = parse_jwt(token)
            if bool(self.AUTHORIZED_OKTA_GROUPS & set(token_data.groups)):
                request.state.user = token_data
                response = await call_next(request)
            else:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        except (AttributeError, HTTPException, JWTError):
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "message": "Unauthorized. If developing locally, see the README for instructions on creating a JWT token."
                },
            )
        return response

    def parse_header(self, request: Request):
        return request.headers.get("Authorization").split(" ")[1]
