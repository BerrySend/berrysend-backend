from pydantic import BaseModel, Field

class AuthenticatedUserResponse(BaseModel):
    """
    Response schema for authentication operations.
    
    This schema represents the data returned after successful
    sign-up or sign-in operations, including the access token.
    
    Attributes:
        id (int): The user's unique identifier
        full_name (str): The user's complete name
        email (str): The user's email address
        token (str): JWT access token for authenticated requests
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
    
    token: str = Field(
        ...,
        description="JWT access token for authenticated requests. Copy this token and use it in the Authorization header as: Bearer <token>",
        example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "fbdbc4f3-fa3f-4008-b4e7-915f246b4ea7",
                "full_name": "John Doe",
                "email": "john.doe@example.com",
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
            }
        }
