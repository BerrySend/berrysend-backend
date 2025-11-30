from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped

from app.shared.infrastructure.models.base_model import BaseModelORM

class UserModel(BaseModelORM):
    """
    ORM model for the user's table.
    
    This model represents the database schema for user entities
    and is used by SQLAlchemy for persistence operations.
    
    Attributes:
        full_name (str): The user's complete name
        email (str): The unique email address of the user
        hashed_password (str): The hashed password of the user
    """
    __tablename__ = "users"

    full_name: Mapped[str] = Column(String(100), nullable=False)
    email: Mapped[str] = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = Column(String(255), nullable=False)