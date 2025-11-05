"""
Application service for user management.
"""
from sqlalchemy.ext.asyncio import AsyncSession

from app.iam.domain.models.user import User
from app.iam.domain.services.user_service import UserService
from app.iam.infrastructure.hashing.hashing_service import HashingService
from app.iam.infrastructure.repositories.user_repository import UserRepository
from app.iam.infrastructure.tokens.token_service import TokenService

class UserApplicationService:
    def __init__(self, db: AsyncSession):
        """
        Initialize the user application service with user service, user repository, hashing service and token service.

        :param db: The database session.
        """
        self.user_service = UserService()
        self.user_repository = UserRepository(db)
        self.hashing_service = HashingService()
        self.token_service = TokenService()

    async def sign_up(self, email: str, password: str) -> User:
        """
        Creates a new user.

        :param email: The email address of the user.
        :param password: The password of the user.
        :return: The newly created user.
        """
        if await self.user_repository.exists_by_email(email):
            raise ValueError("User with this email already exists")

        hashed_password = self.hashing_service.hash(password)
        user = self.user_service.create_user(email, hashed_password)
        return await self.user_repository.create(user)

    async def sign_in(self, email: str, password: str) -> dict[str, str]:
        """
        Signs in a user.

        :param email: The email address of the user.
        :param password: The password of the user.
        :return: The access token and the token type.
        """
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise ValueError("Invalid credentials")

        if not self.hashing_service.verify(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        access_token = self.token_service.create_access_token({"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    async def change_password(self, user_id: str, old_password: str, new_password: str) -> None:
        """
        Change the password of a user.

        :param user_id: The id of the user.
        :param old_password: The old password.
        :param new_password: The new password.
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")

        if not self.hashing_service.verify(old_password, user.hashed_password):
            raise ValueError("Incorrect current password")

        new_hashed_password = self.hashing_service.hash(new_password)
        user.hashed_password = new_hashed_password
        await self.user_repository.update(user)