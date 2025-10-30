from pydantic import BaseModel

class SignInRequest(BaseModel):
    """
    SignInRequest represents the data required for a user to sign in.

    Attributes:
        username (str): The username of the user.
        password (str): The password of the user.
    """
    username: str
    password: str