"""
Authentication Middleware

Provides dependency functions for protecting routes with JWT authentication.
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.services.auth import auth_service
from src.models.database import User
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# HTTP Bearer token security scheme
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency function to get the current authenticated user.

    Extracts and validates JWT token from Authorization header,
    then retrieves the user from the database.

    Args:
        credentials: HTTP Bearer credentials from request header
        db: Database session

    Returns:
        Authenticated User object

    Raises:
        HTTPException: If token is invalid or user not found

    Usage:
        @router.get("/protected")
        async def protected_route(user: User = Depends(get_current_user)):
            return {"user_id": user.id}
    """
    # Extract token
    token = credentials.credentials

    # Verify token
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Extract user ID from token
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Retrieve user from database
    user = auth_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive"
        )

    return user


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency function to optionally get the current authenticated user.

    Similar to get_current_user, but returns None if no token is provided
    instead of raising an exception. Useful for routes that work with or
    without authentication.

    Args:
        credentials: Optional HTTP Bearer credentials from request header
        db: Database session

    Returns:
        Authenticated User object if token is valid, None otherwise

    Usage:
        @router.get("/optional-auth")
        async def optional_auth_route(user: Optional[User] = Depends(get_current_user_optional)):
            if user:
                return {"message": f"Hello, {user.email}"}
            return {"message": "Hello, guest"}
    """
    if not credentials:
        return None

    try:
        # Extract token
        token = credentials.credentials

        # Verify token
        payload = auth_service.verify_token(token)
        if not payload:
            return None

        # Extract user ID from token
        user_id = payload.get("sub")
        if not user_id:
            return None

        # Retrieve user from database
        user = auth_service.get_user_by_id(db, user_id)
        if not user or not user.is_active:
            return None

        return user

    except Exception as e:
        logger.warning(f"Optional auth failed: {e}")
        return None
