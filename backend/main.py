from beanie import init_beanie
from motor import motor_asyncio

from api.core.config import get_settings
from api.core.factory import create_app
from api.model.entitlement import Entitlement

settings = get_settings()
app = create_app(settings)


@app.on_event("startup")
async def startup_db_client():
    client = motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(
        database=client[settings.mongo_db_name], document_models=[Entitlement]
    )
