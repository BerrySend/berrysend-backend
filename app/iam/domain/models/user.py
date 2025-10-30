"""
User domain entity for IAM context.
"""
from dataclasses import dataclass

from app.shared.domain.models.base_entity import BaseEntity

@dataclass
class User(BaseEntity):
    """
    User is a class that represents a user in the IAM context.

    Attributes:
        email (str): the unique email address of the user
        hashed_password (str): the hashed password of the user
    """
    email: str
    hashed_password: str