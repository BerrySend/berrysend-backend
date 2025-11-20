from pydantic import BaseModel, Field

class UserResponse(BaseModel):
    """
    Response schema for user data without an authentication token.
    
    This schema represents basic user information returned
    after registration or when retrieving user data.
    
    Attributes:
        id (str): The user's unique identifier (UUID)
        full_name (str): The user's complete name
        email (str): The user's email address
    """
    
    id: str = Field(
        ...,
        description="The user's unique identifier (UUID)",
        example="fbdbc4f3-fa3f-4008-b4e7-915f246b4ea7"
    )
    
    full_name: str = Field(
        ...,
        description="The user's complete name",
        example="John Doe"
    )
    
    email: str = Field(
        ...,
        description="The user's email address",
        example="john.doe@example.com"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "fbdbc4f3-fa3f-4008-b4e7-915f246b4ea7",
                "full_name": "John Doe",
                "email": "john.doe@example.com"
            }
        }
