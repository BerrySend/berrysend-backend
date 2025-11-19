from pydantic import BaseModel, Field

class SignInRequest(BaseModel):
    """
    Request schema for user authentication.
    
    This schema defines the credentials required to authenticate
    and obtain an access token.
    
    Attributes:
        email (str): The user's email address
        password (str): The user's password
    """
    
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
        description="The user's password",
        example="SecurePass123"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "john.doe@example.com",
                "password": "SecurePass123"
            }
        }