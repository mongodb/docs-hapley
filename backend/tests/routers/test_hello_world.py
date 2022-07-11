from ..base import FastApiTest

client = FastApiTest().client

def test_hello_world():
  response = client.get("hello")

  assert response.status_code == 200
  assert response.json() == {
    "message": "Hello World"
  }
