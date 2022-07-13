from jose import jwt
from datetime import datetime as dt
from dataclasses import dataclass


@dataclass
class TokenData:
    email: str
    groups: list
    exp: dt
    username: str


def parse_jwt(token: str) -> TokenData:
    jwt_mappings: dict[str, str] = {
        "email": "email",
        "groups": "groups",
        "sub": "username",
    }
    payload: dict = jwt.get_unverified_claims(token)
    filtered_payload = {jwt_mappings[key]: payload[key] for key in jwt_mappings.keys()}
    raw_exp_time: int = payload.pop("exp")
    return TokenData(**filtered_payload, exp=dt.fromtimestamp(raw_exp_time))
