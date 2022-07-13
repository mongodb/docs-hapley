from fastapi.testclient import TestClient
from fastapi import FastAPI

from main import app


class FastApiTest(TestClient):
    def __init__(self, fastapi_app: FastAPI = app):
        super().__init__(fastapi_app)
        self.base_url += "/api/v1/"

    # TestClient uses urljoin, which requires a trailing slash on base_url
    # and no leading slash on the second arg. https://stackoverflow.com/questions/69166262/fastapi-adding-route-prefix-to-testclient
    def trim_leading_slash(self, path):
        if path.startswith("/"):
            path = path[1:]
        return path

    def get(self, path: str, **kwargs):
        return super().get(self.base_url + self.trim_leading_slash(path), **kwargs)
