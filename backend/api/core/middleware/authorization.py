from fastapi import Request, status
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from ..util.jwt import TokenData, parse_jwt


# Implement custom middleware by overriding BaseHTTPMiddleware.dispatch
class Authorization(BaseHTTPMiddleware):

    AUTHORIZED_OKTA_GROUPS: set = set(["10gen-docs-platform"])

    async def dispatch(self, request: Request, call_next):
        if request.headers.get("Authorization"):
            token = request.headers.get("Authorization").split(" ")[1]
            token_data: TokenData = parse_jwt(token)

        try:
            if bool(self.AUTHORIZED_OKTA_GROUPS & set(token_data.groups)):
                request.state.user = token_data
                response = await call_next(request)
        except UnboundLocalError:
            response = JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={"message": "Unauthorized"},
            )
        return response
