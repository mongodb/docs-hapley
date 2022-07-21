from fastapi import APIRouter

from .routes import repos, root, sample_token

router = APIRouter()
router.include_router(root.router)
router.include_router(sample_token.router)
router.include_router(repos.router, prefix="/repos")
