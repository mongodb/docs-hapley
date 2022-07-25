from beanie import Document


class Entitlement(Document):
    class Settings:
        name = "entitlements"

    email: str
    github_username: str
    repos: list[str]
    slack_user_id: str
    okta_id: str | None
