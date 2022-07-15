from ....core.config import get_settings
from ....core.middleware.authorization import Authorization
from ...base import FastApiTest

"""
    Tests custom middleware that requires a valid
    JWT token to access the API. Sample token endpoint does
    not require authorization.
"""

unauthorized_client = FastApiTest(with_auth=False)
authorized_client = FastApiTest()


def test_sample_token():
    response = unauthorized_client.get("/sample-token?email=foo@gmail.com&username=foo")

    assert response.status_code == 200
    assert response.json()["token"] is not None


def test_sample_jwt():
    settings = get_settings()
    token_response = unauthorized_client.get(
        "/sample-token?email=foo@gmail.com&username=foo"
    )
    unauthorized_client.headers = {
        "Authorization": "Bearer " + token_response.json()["token"]
    }

    response = unauthorized_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "app_name": settings.app_name,
        "description": settings.description,
    }


def test_invalid_jwt():
    unauthorized_client.headers = {"Authorization": "Bearer " + "invalid_token"}

    response = unauthorized_client.get("/")
    assert response.status_code == 401
    assert "Error decoding token claims." in response.json()["message"]
    assert (
        "See README for instructions on creating a JWT token if developing locally"
        in response.json()["message"]
    )


def test_invalid_okta_group():
    unauthorized_jwt = Authorization.build_sample_token(
        email="foo@mongodb.com", username="foo", is_authorized=False
    )
    unauthorized_client.headers = {"Authorization": "Bearer " + unauthorized_jwt}

    response = unauthorized_client.get("/")
    assert response.status_code == 401
    assert (
        "User is not authorized to access this resource." in response.json()["message"]
    )
    assert (
        "Ensure you are a member of an authorized Okta group"
        in response.json()["message"]
    )


def test_valid_jwt():
    authorized_client = FastApiTest()

    response = authorized_client.get("/")
    assert response.status_code == 200
