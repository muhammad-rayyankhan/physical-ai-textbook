"""
Authentication Service

Handles user authentication, password hashing, and JWT token generation.
"""

from typing import Optional
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from src.core.config import settings
from src.models.database import User
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


class AuthService:
    """Service for authentication operations."""

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password string
        """
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against a hash.

        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, user_id: str, email: str) -> str:
        """
        Create a JWT access token.

        Args:
            user_id: User's unique identifier
            email: User's email address

        Returns:
            JWT token string
        """
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {
            "sub": str(user_id),
            "email": email,
            "exp": expire
        }
        encoded_jwt = jwt.encode(to_encode, settings.AUTH_SECRET, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[dict]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded token payload if valid, None otherwise
        """
        try:
            payload = jwt.decode(token, settings.AUTH_SECRET, algorithms=[ALGORITHM])
            return payload
        except JWTError as e:
            logger.error(f"Token verification failed: {e}")
            return None

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Retrieve a user by email address.

        Args:
            db: Database session
            email: User's email address

        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, user_id: str) -> Optional[User]:
        """
        Retrieve a user by ID.

        Args:
            db: Database session
            user_id: User's unique identifier

        Returns:
            User object if found, None otherwise
        """
        return db.query(User).filter(User.id == user_id).first()

    def create_user(
        self,
        db: Session,
        email: str,
        password: str,
        name: Optional[str] = None,
        background: Optional[str] = None
    ) -> User:
        """
        Create a new user account.

        Args:
            db: Database session
            email: User's email address
            password: Plain text password
            name: User's name (optional)
            background: User's background for personalization (optional)

        Returns:
            Created User object

        Raises:
            ValueError: If user with email already exists
        """
        # Check if user already exists
        existing_user = self.get_user_by_email(db, email)
        if existing_user:
            raise ValueError(f"User with email {email} already exists")

        # Hash password
        password_hash = self.hash_password(password)

        # Create user
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            background=background,
            is_active=True
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        logger.info(f"Created new user: {email}")
        return user

    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate a user with email and password.

        Args:
            db: Database session
            email: User's email address
            password: Plain text password

        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.get_user_by_email(db, email)
        if not user:
            logger.warning(f"Authentication failed: User {email} not found")
            return None

        if not user.is_active:
            logger.warning(f"Authentication failed: User {email} is inactive")
            return None

        if not self.verify_password(password, user.password_hash):
            logger.warning(f"Authentication failed: Invalid password for {email}")
            return None

        logger.info(f"User authenticated successfully: {email}")
        return user


# Global service instance
auth_service = AuthService()
