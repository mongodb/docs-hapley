from api.core.config import Settings
from api.core.factory import create_app

settings = Settings()
app = create_app(settings)
