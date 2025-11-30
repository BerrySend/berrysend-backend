"""
User Service class with methods for user management.
"""
import re
from app.iam.domain.models.user import User

class UserService:
    """
    Domain service for user-related business logic.
    
    This service encapsulates validation rules and business operations
    that don't naturally fit within the User entity itself.
    """
    
    def __init__(self):
        """
        Initializes the user service.
        """
        pass

    @staticmethod
    def validate_full_name(full_name: str) -> None:
        """
        Validate that the full name meets business requirements.
        
        Args:
            full_name: The name to validate
            
        Raises:
            ValueError: If the name is invalid
        """
        if not full_name or not full_name.strip():
            raise ValueError("Full name is required")
        
        if len(full_name.strip()) < 3:
            raise ValueError("Full name must be at least 3 characters long")
        
        if len(full_name) > 100:
            raise ValueError("Full name must not exceed 100 characters")
    
    @staticmethod
    def validate_email(email: str) -> None:
        """
        Validate that the email has a basic valid format.
        
        Args:
            email: The email to validate
            
        Raises:
            ValueError: If the email format is invalid
        """
        if not email or not email.strip():
            raise ValueError("Email is required")
        
        # Basic email format validation (allows any format like example@example.com)
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            raise ValueError("Invalid email format")
    
    @staticmethod
    def validate_password(password: str) -> None:
        """
        Validate that the password meets security requirements.
        
        Args:
            password: The password to validate
            
        Raises:
            ValueError: If the password doesn't meet requirements
        """
        if not password:
            raise ValueError("Password is required")
        
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Bcrypt has a 72-byte limit, so we enforce a 72-character limit
        if len(password) > 72:
            raise ValueError("Password must not exceed 72 characters")
        
        # Check for at least one uppercase letter
        if not re.search(r'[A-Z]', password):
            raise ValueError("Password must contain at least one uppercase letter")
        
        # Check for at least one lowercase letter
        if not re.search(r'[a-z]', password):
            raise ValueError("Password must contain at least one lowercase letter")
        
        # Check for at least one digit
        if not re.search(r'\d', password):
            raise ValueError("Password must contain at least one number")
    
    @staticmethod
    def validate_password_confirmation(password: str, confirm_password: str) -> None:
        """
        Validate that password and confirmation match.
        
        Args:
            password: The original password
            confirm_password: The confirmation password
            
        Raises:
            ValueError: If passwords don't match
        """
        if password != confirm_password:
            raise ValueError("Passwords do not match")

    @staticmethod
    def create_user(full_name: str, email: str, hashed_password: str) -> "User":
        """
        Creates a new user with validation.

        :param full_name: The user's complete name
        :param email: The email address of the user.
        :param hashed_password: The hashed password of the user.
        :return: A new instance of the User class.
        """
        UserService.validate_full_name(full_name)
        UserService.validate_email(email)

        return User(
            full_name=full_name.strip(),
            email=email.strip().lower(),
            hashed_password=hashed_password
        )

    @staticmethod
    def change_password(user: User, new_hashed_password: str) -> None:
        """
        Changes the password of a user.

        :param user: The user whose password is to be changed.
        :param new_hashed_password: The new hashed password.
        """
        if not new_hashed_password or not new_hashed_password.strip():
            raise ValueError("Password cannot be empty")

        if new_hashed_password == user.hashed_password:
            raise ValueError("New password cannot be the same as the old one")

        user.update_password(new_hashed_password)