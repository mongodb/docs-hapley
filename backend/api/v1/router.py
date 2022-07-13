from fastapi import APIRouter

from .routes import root, login

router = APIRouter()
router.include_router(root.router)
router.include_router(login.router)
