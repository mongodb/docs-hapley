from api.tests.base import FastApiTest


def test_repos_get():
    with FastApiTest() as client:
        response = client.get("/repos")
        assert response.status_code == 200
        assert response.json()["repos"] == ["docs-landing"]
