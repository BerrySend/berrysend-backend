"""
User domain entity for IAM context.
"""
from dataclasses import dataclass
from datetime import datetime

from app.shared.domain.models.base_entity import BaseEntity

@dataclass
class User(BaseEntity):
    """
    Represents a user in the system.
    
    This is a domain entity that encapsulates the business rules
    and invariants for user management.
    
    Attributes:
        full_name (str): The user's complete name
        email (str): The user's email address (used for authentication)
        hashed_password (str): The user's hashed password
    """
    full_name: str
    email: str
    hashed_password: str
    
    def update_password(self, new_hashed_password: str) -> None:
        """
        Update the user's password.
        
        Args:
            new_hashed_password: The new hashed password
        """
        self.hashed_password = new_hashed_password
        self.updated_at = datetime.now()