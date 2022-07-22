from api.core.config import Settings
from api.core.factory import create_app
from api.database import start_db_client

settings = Settings()
app = create_app(settings)


@app.on_event("startup")
async def startup_app():
    await start_db_client(settings)
