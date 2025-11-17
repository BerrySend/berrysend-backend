from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.iam.application.user_application_service import UserApplicationService
from app.iam.interfaces.resources.sign_in_request import SignInRequest
from app.iam.interfaces.resources.sign_up_request import SignUpRequest
from app.iam.interfaces.resources.authenticated_user_response import AuthenticatedUserResponse
from app.iam.interfaces.resources.user_response import UserResponse
from app.shared.infrastructure.persistence.session_generator import get_db

# Create router for authentication endpoints
auth_router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@auth_router.post(
    "/sign-up",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with full name, email, and password. Returns user data without token.",
    responses={
        201: {
            "description": "User successfully created",
            "content": {
                "application/json": {
                    "example": {
                        "id": "fbdbc4f3-fa3f-4008-b4e7-915f246b4ea7",
                        "full_name": "John Doe",
                        "email": "john.doe@example.com"
                    }
                }
            }
        },
        400: {"description": "Validation error or email already registered"},
        500: {"description": "Internal server error"}
    }
)
async def sign_up(
    request: SignUpRequest,
    session: AsyncSession = Depends(get_db)
) -> UserResponse:
    """
    Register a new user account.
    
    This endpoint creates a new user with the provided information,
    validates all input data, and hashes the password securely.
    To obtain an access token, use the sign-in endpoint after registration.
    
    Args:
        request: Sign-up request containing user data
        session: Database session (injected)
        
    Returns:
        User data without access token
        
    Raises:
        HTTPException: If validation fails or email already exists
    """
    try:
        user_service = UserApplicationService(session)
        user = await user_service.sign_up(
            full_name=request.full_name,
            email=request.email,
            password=request.password,
            confirm_password=request.confirm_password
        )
        
        return UserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log the full error for debugging
        import traceback
        print(f"Error during sign-up: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred during registration: {str(e)}"
        )


@auth_router.post(
    "/sign-in",
    response_model=AuthenticatedUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate user",
    description="Sign in with email and password. Returns user data and access token.",
    responses={
        200: {
            "description": "Successfully authenticated",
            "content": {
                "application/json": {
                    "example": {
                        "id": "fbdbc4f3-fa3f-4008-b4e7-915f246b4ea7",
                        "full_name": "John Doe",
                        "email": "john.doe@example.com",
                        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                    }
                }
            }
        },
        400: {"description": "Invalid credentials"},
        500: {"description": "Internal server error"}
    }
)
async def sign_in(
    request: SignInRequest,
    session: AsyncSession = Depends(get_db)
) -> AuthenticatedUserResponse:
    """
    Authenticate a user and obtain an access token.
    
    This endpoint validates user credentials and returns an access token
    that can be used to authenticate subsequent requests to protected endpoints.
    
    Args:
        request: Sign-in request containing credentials
        session: Database session (injected)
        
    Returns:
        User data with access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        user_service = UserApplicationService(session)
        user, token = await user_service.sign_in(
            email=request.email,
            password=request.password
        )
        
        return AuthenticatedUserResponse(
            id=user.id,
            full_name=user.full_name,
            email=user.email,
            token=token
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during authentication"
        )