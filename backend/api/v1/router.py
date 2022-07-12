from fastapi import APIRouter

from .routes import hello_world

router = APIRouter()
router.include_router(hello_world.router)
