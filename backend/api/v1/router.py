from fastapi import APIRouter

from .routes import repos, hello_world

router = APIRouter()
router.include_router(repos.router, prefix='/repos', tags=['repos'])
router.include_router(hello_world.router)
