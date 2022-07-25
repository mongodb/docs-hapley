from fastapi.testclient import TestClient

from api.core.config import Settings
from api.core.factory import create_app
from api.database import start_db_client

from ..core.middleware.authorization import Authorization

settings = Settings(mongo_uri="mongodb://localhost:27017", mongo_db_name="hapley_test")
test_app = create_app(settings)


@test_app.on_event("startup")
async def startup_test_app():
    await start_db_client(settings)


# Custom TestClient that accounts for custom middleware & API structure
class FastApiTest(TestClient):
    def __init__(self, with_auth: bool = True):
        super().__init__(test_app)
        self.base_url += "/api/v1/"
        if with_auth:
            test_username = "foo"
            token = Authorization.build_sample_token(
                email="foo@gmail.com", username=test_username
            )

            # Set cookies that are automatically set through CorpSecure
            self.cookies["auth_user"] = test_username
            self.cookies["auth_token"] = token

    # TestClient uses urljoin, which requires a trailing slash on base_url
    # and no leading slash on the second arg. https://stackoverflow.com/questions/69166262/fastapi-adding-route-prefix-to-testclient
    def trim_leading_slash(self, path):
        if path.startswith("/"):
            path = path[1:]
        return path

    def get(self, path: str, **kwargs):
        return super().get(self.base_url + self.trim_leading_slash(path), **kwargs)
