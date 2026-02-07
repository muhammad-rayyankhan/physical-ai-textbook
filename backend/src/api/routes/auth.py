"""
Authentication Routes

Handles user signup, login, and logout endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
from src.core.database import get_db
from src.services.auth import auth_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])


# Request/Response Models
class SignupRequest(BaseModel):
    """Request model for user signup."""
    email: EmailStr
    password: str
    name: Optional[str] = None
    background: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123",
                "name": "John Doe",
                "background": "Computer Science student interested in robotics"
            }
        }


class LoginRequest(BaseModel):
    """Request model for user login."""
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "securepassword123"
            }
        }


class AuthResponse(BaseModel):
    """Response model for authentication endpoints."""
    access_token: str
    token_type: str = "bearer"
    user: dict

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "user@example.com",
                    "name": "John Doe"
                }
            }
        }


class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    """
    Create a new user account.

    Args:
        request: Signup request with email, password, name, and background
        db: Database session

    Returns:
        AuthResponse with access token and user information

    Raises:
        HTTPException: If user already exists or validation fails
    """
    try:
        # Validate password strength
        if len(request.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long"
            )

        # Create user
        user = auth_service.create_user(
            db=db,
            email=request.email,
            password=request.password,
            name=request.name,
            background=request.background
        )

        # Generate access token
        access_token = auth_service.create_access_token(
            user_id=str(user.id),
            email=user.email
        )

        logger.info(f"User signed up successfully: {user.email}")

        return AuthResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "background": user.background,
                "created_at": user.created_at.isoformat()
            }
        )

    except ValueError as e:
        # User already exists
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Signup error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate user and return access token.

    Args:
        request: Login request with email and password
        db: Database session

    Returns:
        AuthResponse with access token and user information

    Raises:
        HTTPException: If authentication fails
    """
    # Authenticate user
    user = auth_service.authenticate_user(
        db=db,
        email=request.email,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generate access token
    access_token = auth_service.create_access_token(
        user_id=str(user.id),
        email=user.email
    )

    logger.info(f"User logged in successfully: {user.email}")

    return AuthResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "background": user.background,
            "created_at": user.created_at.isoformat()
        }
    )


@router.post("/logout", response_model=MessageResponse)
async def logout():
    """
    Logout user (client-side token invalidation).

    Note: JWT tokens are stateless, so logout is handled client-side
    by removing the token from storage.

    Returns:
        Success message
    """
    return MessageResponse(message="Logged out successfully")


@router.get("/me", response_model=dict)
async def get_current_user_info(db: Session = Depends(get_db)):
    """
    Get current authenticated user information.

    This endpoint requires authentication (to be implemented with middleware).

    Args:
        db: Database session

    Returns:
        User information
    """
    # TODO: Implement with auth middleware
    # For now, return placeholder
    return {
        "message": "This endpoint requires authentication middleware"
    }
