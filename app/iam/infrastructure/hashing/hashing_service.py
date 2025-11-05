"""
Hashing Service for hashing passwords of the users.
"""
from passlib.context import CryptContext

# Creates a context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class HashingService:
    @staticmethod
    def hash(password: str) -> str:
        """
        Hashes a password

        :param password: The password to be hashed
        :return: The hashed password
        """
        return pwd_context.hash(password)

    @staticmethod
    def verify(plain_password: str, hashed_password: str) -> bool:
        """
        Compares a plain password with a hashed password

        :param plain_password: A plain password to be compared
        :param hashed_password: The hashed password to be compared
        :return: True if the passwords match, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)