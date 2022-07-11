from fastapi.testclient import TestClient
from main import app

class FastApiTest():
    def __init__(self):
        self.client = TestClient(app)
        self.client.base_url += "/api/v1"
        self.client.base_url = self.client.base_url.rstrip("/") + "/"
