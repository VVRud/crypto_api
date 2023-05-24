from datetime import datetime, timedelta

import config
import models
from fastapi import HTTPException
from jose import JWTError, jwt
from modules.database import Database
from modules.keys_loader import KeysLoader
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status


class Auth:
    """
    Authentication related module. Contains methods for user validation,
    password hashing, creating tokens and validating them.
    """

    JWT_ALGORITHM = config.JWT_ALGORITHM
    JWT_EXPIRE = config.JWT_EXPIRE

    PWD_ALGORITHM = config.PWD_ALGORITHM

    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=[Auth.PWD_ALGORITHM], deprecated="auto"
        )
        self.jwt_secret_token = (
            KeysLoader.get_keys_loader().load_jwt_secret_token()
        )

    @classmethod
    def get_auth(cls):
        """Get authentication class/context."""
        return cls()

    async def authenticate_user(
        self, session: AsyncSession, username: str, password: str
    ) -> None | models.User:
        """Authenticate user and return its instance if exists."""
        db_user = await Database.get_user(session, username)
        if not db_user:
            return None
        if not self.verify_password(password, db_user.password):
            return None
        return db_user

    def get_password_hash(self, password: str) -> str:
        """Get hashed password."""
        return self.pwd_context.hash(password)

    def verify_password(
        self, plain_password: str, hashed_password: str
    ) -> bool:
        """Verify password hashes."""
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(
        self, username: str, expires_delta: timedelta | None = None
    ) -> str:
        """Create JWT access token."""
        to_encode = {"sub": username}
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            self.jwt_secret_token,
            algorithm=self.JWT_ALGORITHM,
        )
        return encoded_jwt

    async def get_current_user(
        self, session: AsyncSession, token: str
    ) -> models.User:
        """Retrieve current user from JWT token."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, self.jwt_secret_token, algorithms=[self.JWT_ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = await Database.get_user(sess=session, username=username)
        if user is None:
            raise credentials_exception
        return user
