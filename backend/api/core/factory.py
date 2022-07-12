from fastapi import FastAPI
from .config import Settings
from starlette.middleware.cors import CORSMiddleware
from ..router import router as api_router
from os import getenv
from .middleware.authorization import Authorization

def create_app(settings: Settings, environment: str = getenv("ENVIRONMENT")) -> FastAPI:
    app: FastAPI = FastAPI(settings=settings)
    app.include_router(api_router, prefix='/api')

    # Attach necessary middleware depending on the environment
    env_middleware_map: dict[str|function] = {
        "development": cors_middleware,
        "production": authorization_middleware,
        "staging": authorization_middleware
    }
    env_middleware_map[environment or "development"](app)
    return app

def cors_middleware(app: FastAPI) -> None:
    origins: list[str] = ["http://localhost:3000"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

def authorization_middleware(app) -> None:
    app.add_middleware(Authorization)
