from dataclasses import dataclass
from datetime import datetime
import uuid

@dataclass
class User:
    """
    User is a class that represents a user in the IAM context.

    Attributes:
        email (str): the unique email address of the user
        hashed_password (str): the hashed password of the user
        created_at (datetime): the date and time the user was created
        updated_at (datetime): the date and time the user was updated
        id (uuid): the unique id of the user
    """
    email: str
    hashed_password: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()
    id: uuid.UUID = uuid.uuid4()

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