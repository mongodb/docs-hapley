from fastapi import APIRouter

from .routes import root

router = APIRouter()
router.include_router(root.router)
