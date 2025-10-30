"""
User Service class with methods for user management.
"""
from app.iam.domain.models.user import User

class UserService:
    def __init__(self):
        """
        Initializes the user service.
        """
        pass

    @staticmethod
    def create_user(email: str, hashed_password: str) -> "User":
        """
        Creates a new user.

        :param email: The email address of the user.
        :param hashed_password: The hashed password of the user.
        :return: A new instance of the User class.
        """
        try:
            if email.strip() == "":
                raise ValueError("Email cannot be empty.")
            if hashed_password.strip() == "":
                raise ValueError("Password cannot be empty.")
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        return User(email=email, hashed_password=hashed_password)

    @staticmethod
    def change_password(user: User, new_hashed_password: str) -> None:
        """
        Changes the password of a user.

        :param user: The user whose password is to be changed.
        :param new_hashed_password: The new hashed password.
        """
        try:
            if new_hashed_password.strip() == "":
                raise ValueError("Password cannot be empty.")

            if new_hashed_password == user.hashed_password:
                raise ValueError("New password cannot be the same as the old one.")
        except (ValueError, TypeError):
            raise ValueError("Invalid data format.")

        user.hashed_password = new_hashed_password