"""
Base Model Class for ORM with common columns.
"""
import uuid

from sqlalchemy import String, Column
from sqlalchemy.orm import mapped_column, Mapped
from datetime import datetime

from app.shared.infrastructure.models.declarative_base import ORMBase

class BaseModelORM(ORMBase):
    """
    Base Model Class for the ORM that defines common columns.

    Attributes:
        id (str): the unique identifier of the entity
        created_at (datetime): the creation date and time of the entity
        updated_at (datetime): the last update date and time of the entity
    """
    __abstract__ = True

    id: Mapped[str] = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now)