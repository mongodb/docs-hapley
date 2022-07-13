from ...base import FastApiTest
from ....core.factory import create_app
from ....core.config import Settings

settings = Settings()

"""
    Tests custom middleware that requires a valid
    JWT token in non-dev/test environments.
"""


def test_root_authorized():
    client = FastApiTest()
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"app_name": settings.app_name}


# Manually create new FastAPI app with authroization middleware
# by passing in production environment
def test_root_unauthorized():
    app = create_app(settings, "production")
    client = FastApiTest(fastapi_app=app)
    response = client.get("/")

    assert response.status_code == 401
    assert response.json() == {"message": "Unauthorized"}
