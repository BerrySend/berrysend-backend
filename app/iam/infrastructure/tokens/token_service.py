import jwt
from datetime import datetime, timedelta
from typing import Any

from dotenv import dotenv_values

config = dotenv_values("development.env")

SECRET_KEY = config["SECRET_KEY"]
ALGORITHM = config["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = int(config["ACCESS_TOKEN_EXPIRE_MINUTES"])

class TokenService:
    @staticmethod
    def create_access_token(data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])