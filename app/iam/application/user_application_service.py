"""
Application service for user management.
"""
from typing import Tuple
from sqlalchemy.ext.asyncio import AsyncSession

from app.iam.domain.models.user import User
from app.iam.domain.services.user_service import UserService
from app.iam.infrastructure.hashing.hashing_service import HashingService
from app.iam.infrastructure.repositories.user_repository import UserRepository
from app.iam.infrastructure.tokens.token_service import TokenService

class UserApplicationService:
    """
    Application service for user-related use cases.
    
    This service orchestrates domain logic, infrastructure services,
    and repositories to implement complete use cases for the IAM bounded context.
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize the UserApplicationService with required dependencies.

        :param db: The database session.
        """
        self.db = db
        self.user_service = UserService()
        self.user_repository = UserRepository(db)
        self.hashing_service = HashingService()
        self.token_service = TokenService()

    async def sign_up(
        self,
        full_name: str,
        email: str,
        password: str,
        confirm_password: str
    ) -> User:
        """
        Register a new user in the system.
        
        This use case validates user data, checks for duplicates,
        hashes the password, and persists the user.

        :param full_name: The user's complete name
        :param email: The email address of the user.
        :param password: The password of the user.
        :param confirm_password: Password confirmation
        :return: The created User entity
        :raises ValueError: If validation fails or email already exists
        """
        # Validate password and confirmation
        self.user_service.validate_password(password)
        self.user_service.validate_password_confirmation(password, confirm_password)
        
        # Check if email already exists
        if await self.user_repository.exists_by_email(email):
            raise ValueError("Email already registered")

        # Hash password before persisting
        hashed_password = self.hashing_service.hash(password)
        
        # Create user with domain validation
        user = self.user_service.create_user(full_name, email, hashed_password)
        
        # Persist user
        created_user = await self.user_repository.create(user)
        
        return created_user

    async def sign_in(self, email: str, password: str) -> Tuple[User, str]:
        """
        Authenticate a user and generate an access token.
        
        This use case validates credentials and generates a JWT token
        for authenticated access to protected endpoints.

        :param email: The email address of the user.
        :param password: The password of the user.
        :return: A tuple containing the authenticated User and their JWT token
        :raises ValueError: If credentials are invalid
        """
        # Find user by email
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        # Verify password
        if not self.hashing_service.verify(password, user.hashed_password):
            raise ValueError("Invalid credentials")

        # Generate access token
        token = self.token_service.create_access_token({"sub": str(user.id)})
        
        return user, token

    async def get_user_by_id(self, user_id: int) -> User:
        """
        Retrieve a user by their ID.
        
        Args:
            user_id: The ID of the user to retrieve
            
        Returns:
            The User entity
            
        Raises:
            ValueError: If user not found
        """
        user = await self.user_repository.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user

    async def change_password(self, user_id: int, old_password: str, new_password: str) -> None:
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
        
        # Validate new password
        self.user_service.validate_password(new_password)

        new_hashed_password = self.hashing_service.hash(new_password)
        self.user_service.change_password(user, new_hashed_password)
        await self.user_repository.update(user)