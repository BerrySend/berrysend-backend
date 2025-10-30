from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from app.shared.infrastructure.models.base_model import BaseModelORM

class UserModel(BaseModelORM):
    """
    Model class for mapping the user entity fields

    Attributes:
        email (str): the unique email address of the user
        hashed_password (str): the hashed password of the user
    """
    __tablename__ = "users"

    email: Mapped[str] = Column(String(255), unique=True, nullable=False)
    hashed_password: Mapped[str] = Column(String(255), nullable=False)