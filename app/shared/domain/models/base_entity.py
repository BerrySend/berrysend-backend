"""
Base class for all entities.
"""
from dataclasses import dataclass, field
import uuid
from datetime import datetime

@dataclass(kw_only=True)
class BaseEntity:
    """
    Base entity class to be inherited by all entities.

    Attributes:
        id (str): the unique identifier of the entity
        created_at (datetime): the creation date and time of the entity
        updated_at (datetime): the last update date and time of the entity
    """
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)