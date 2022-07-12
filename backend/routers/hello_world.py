from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")


@router.get("/hello")
async def read_hello():
    return {"message": "Hello World"}
