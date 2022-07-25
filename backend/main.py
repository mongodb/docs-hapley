from beanie import init_beanie
from motor import motor_asyncio
from pymongo.errors import ConfigurationError, InvalidName

from api.core.config import get_settings
from api.core.factory import create_app
from api.model.entitlement import Entitlement
from api.model.repo import Repo

settings = get_settings()
app = create_app(settings)


@app.on_event("startup")
async def startup_db_client():
    try:
        client = motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
        await init_beanie(
            database=client[settings.mongo_db_name], document_models=[Entitlement, Repo]
        )
    except (ConfigurationError):
        raise ConfigurationError(
            "FastAPI encountered an error on startup. Did you set MONGO_URI in your .env file?"
        )
    except (InvalidName):
        raise InvalidName(
            "FastAPI encountered an error on startup. Did you set MONGO_DB_NAME in your .env file?"
        )
