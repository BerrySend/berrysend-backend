import jwt
from datetime import datetime, timedelta
from typing import Any

from dotenv import dotenv_values
from fastapi import HTTPException
from jwt import ExpiredSignatureError, InvalidTokenError

from app.config import settings

class TokenService:
    @staticmethod
    def create_access_token(data: dict[str, Any]) -> str:
        to_encode = data.copy()
        expire = datetime.now() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except InvalidTokenError:
            raise HTTPException(status_code=401, detail="Invalid token")