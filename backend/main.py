from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import hello_world

app = FastAPI()

# Prevent CORS errors in local development
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(hello_world.router)
