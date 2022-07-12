from fastapi import FastAPI
from .config import Settings
from ..router import router as api_router

def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(settings=settings)
    app.include_router(api_router, prefix='/api')
    return app
