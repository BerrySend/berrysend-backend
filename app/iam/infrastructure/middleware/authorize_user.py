from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.iam.domain.models.user import User
from app.iam.infrastructure.repositories.user_repository import UserRepository
from app.iam.infrastructure.tokens.token_service import TokenService
from app.shared.infrastructure.persistence.session_generator import get_db

# HTTPBearer security scheme for JWT tokens
security = HTTPBearer()

token_service = TokenService()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Args:
        credentials: HTTP Bearer credentials from Authorization header
        db: Database session
        
    Returns:
        The authenticated User entity
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    try:
        payload = token_service.decode_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Invalid token payload"
            )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired token"
        )

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User not found"
        )

    return user