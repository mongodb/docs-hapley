from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from ..router import router as api_router
from .config import Settings
from .metadata.tags import tags_metadata
from .middleware.authorization import Authorization


def create_app(settings: Settings) -> FastAPI:
    app: FastAPI = FastAPI(
        title=settings.app_name,
        description=settings.description,
        openapi_tags=tags_metadata,
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
        redoc_url="/api/v1/redoc",
        settings=settings,
    )
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
