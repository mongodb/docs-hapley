from ...base import FastApiTest
from ....core.config import Settings

settings = Settings()
authorized_client = FastApiTest()

"""
    Tests custom middleware that requires a valid
    JWT token to access the API. Login endpoint does
    not require authorization.
"""


def test_login():
    unauthorized_client = FastApiTest(with_auth=False)
    response = unauthorized_client.get("/login?email=foo@gmail.com&username=foo")

    assert response.status_code == 200
    assert response.json()["token"] is not None


def test_login_jwt():
    client = FastApiTest(with_auth=False)
    token_response = client.get("/login?email=foo@gmail.com&username=foo")
    client.headers = {"Authorization": "Bearer " + token_response.json()["token"]}

    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"app_name": settings.app_name}


def test_invalid_jwt():
    client = FastApiTest(with_auth=False)
    client.headers = {"Authorization": "Bearer " + "invalid_token"}

    response = client.get("/")
    assert response.status_code == 401


def test_valid_jwt():
    client = FastApiTest()

    response = client.get("/")
    assert response.status_code == 200
