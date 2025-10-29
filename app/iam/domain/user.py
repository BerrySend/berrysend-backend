"""
User domain entity for IAM context.
"""
from dataclasses import dataclass

from app.shared.domain.base_entity import BaseEntity

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

    @classmethod
    def create(cls, email: str, hashed_password: str) -> "User":
        """
        Method that creates a new user in the IAM context.

        :param email: The email address for creating the user
        :param hashed_password: The hashed password of the user
        :return: A new instance of User
        """
        return cls(
            email=email,
            hashed_password=hashed_password
        )