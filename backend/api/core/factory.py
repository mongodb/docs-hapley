from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ..router import router as api_router
from .config import Settings
from .middleware.authorization import Authorization


def create_app(settings: Settings) -> FastAPI:
    app: FastAPI = FastAPI(settings=settings)
    app.include_router(api_router, prefix="/api")

    # Attach custom middleware
    cors_middleware(app)
    authorization_middleware(app)

    return app


def cors_middleware(app: FastAPI) -> None:
    origins: list[str] = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def authorization_middleware(app) -> None:
    app.add_middleware(Authorization)
