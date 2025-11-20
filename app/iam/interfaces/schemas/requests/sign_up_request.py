from pydantic import BaseModel, Field

class SignUpRequest(BaseModel):
    """
    Request schema for user registration.
    
    This schema defines the data required to create a new user account
    and includes validation rules for each field.
    
    Attributes:
        full_name (str): The user's complete name
        email (str): The user's email address
        password (str): The user's password
        confirm_password (str): Password confirmation
    """
    
    full_name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The user's complete name",
        example="John Doe"
    )
    
    email: str = Field(
        ...,
        max_length=255,
        description="The user's email address",
        example="john.doe@example.com"
    )
    
    password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="The user's password (min 8 chars, max 72 chars, must include uppercase, lowercase, and number)",
        example="SecurePass123"
    )
    
    confirm_password: str = Field(
        ...,
        min_length=8,
        max_length=72,
        description="Password confirmation (must match password)",
        example="SecurePass123"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "password": "SecurePass123",
                "confirm_password": "SecurePass123"
            }
        }