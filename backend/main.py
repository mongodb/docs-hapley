from api.core.config import get_settings
from api.core.factory import create_app

settings = get_settings()
app = create_app(settings)
