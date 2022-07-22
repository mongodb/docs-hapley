from beanie import init_beanie
from motor import motor_asyncio
from pymongo.errors import ConfigurationError, InvalidName

from api.core.config import Settings
from api.model.entitlement import Entitlement
from api.model.repo import Repo


ALL_DOCUMENT_MODELS = [Entitlement, Repo]


async def start_db_client(settings: Settings):
    try:
        client = motor_asyncio.AsyncIOMotorClient(settings.mongo_uri)
        await init_beanie(
            database=client[settings.mongo_db_name], document_models=ALL_DOCUMENT_MODELS
        )
    except (ConfigurationError):
        raise ConfigurationError(
            "FastAPI encountered an error on startup. Did you set MONGO_URI in your .env file?"
        )
    except (InvalidName):
        raise InvalidName(
            "FastAPI encountered an error on startup. Did you set MONGO_DB_NAME in your .env file?"
        )
