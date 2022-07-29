from api.tests.base import FastApiTest

from .test_versions import generate_random_valid_version

VALID_VERSION_ID: str = "62e187caab5eba28886e74c4"
VALID_ENDPOINT: str = f"/repos/docs/versions/{VALID_VERSION_ID}/"
INVALID_REPO_ENDPOINT: str = f"/repos/foobar/versions/{VALID_VERSION_ID}/"
INVALID_OBJECT_ID_ENDPOINT: str = "/repos/docs/versions/foobar/"
INVALID_VERSION_ENDPOINT: str = "/repos/docs/versions/62e187caab5eba28886e74b1/"


def test_valid_get():
    with FastApiTest() as client:
        response = client.get(VALID_ENDPOINT)
        assert response.status_code == 200
        version = response.json()
        assert len(version["id"]) > 0 and version["id"] == VALID_VERSION_ID


def test_all_methods_invalid_repo_name():
    with FastApiTest() as client:
        http_methods = ["get", "put", "delete"]
        for method in http_methods:
            response = getattr(client, method)(INVALID_REPO_ENDPOINT)
            assert response.status_code == 404
            assert (
                "The repo foobar does not exist." in response.json()["detail"]["errors"]
            )


def test_all_methods_invalid_object_id():
    with FastApiTest() as client:
        http_methods = ["get", "put", "delete"]
        for method in http_methods:
            response = getattr(client, method)(INVALID_OBJECT_ID_ENDPOINT)
            assert response.status_code == 422
            assert (
                "is not a valid 24-byte hex string"
                in response.json()["detail"]["errors"][0]
            )


def test_all_methods_invalid_version_id():
    with FastApiTest() as client:
        http_methods = ["get", "put", "delete"]
        for method in http_methods:
            response = getattr(client, method)(INVALID_VERSION_ENDPOINT)
            assert response.status_code == 404
            assert (
                "The version 62e187caab5eba28886e74b1 does not exist."
                in response.json()["detail"]["errors"]
            )


def test_valid_put():
    with FastApiTest() as client:
        before_update = client.get(VALID_ENDPOINT).json()
        update_payload = generate_random_valid_version()
        response = client.put(VALID_ENDPOINT, json=update_payload)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["id"] == before_update["id"]
        del json_response["id"]
        assert json_response == update_payload


def test_invalid_git_branch_put():
    used_branch_name: str = "3.2"
    with FastApiTest() as client:
        update_payload = client.get(VALID_ENDPOINT).json()
        update_payload["gitBranchName"] = used_branch_name
        response = client.put(VALID_ENDPOINT, json=update_payload)
        assert response.status_code == 422
        assert (
            f"gitBranchName: {used_branch_name} is already in use"
            in response.json()["detail"]["errors"][0]
        )


def test_invalid_url_slug_put():
    with FastApiTest() as client:
        update_payload = client.get(VALID_ENDPOINT).json()
        update_payload["urlSlug"] = "foobar"
        del update_payload["id"]
        response = client.put(VALID_ENDPOINT, json=update_payload)
        assert response.status_code == 422
        assert (
            "urlSlug must match gitBranchName or be an element of url aliases"
            in response.json()["detail"]["errors"][0]
        )


def test_valid_delete():
    with FastApiTest() as client:
        response = client.delete(VALID_ENDPOINT)
        assert response.status_code == 200
        assert response.json()["success"] is True

        response = client.get(VALID_ENDPOINT)
        assert response.status_code == 404
