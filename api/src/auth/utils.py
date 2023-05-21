from datetime import datetime, timedelta

from auth.constants import ALGORITHM
from jose import jwt
from keys_loader import KeysLoader
from models import User
from passlib.context import CryptContext
from schemas import UserPassword

from database import database

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(session, user: UserPassword) -> None | User:
    """Authenticate user and return its instance if exists."""
    db_user = await database.get_user(session, user.username)
    if not db_user:
        return None
    if not verify_password(user.password, db_user.password):
        return None
    return db_user


def verify_password(plain_password: str, hashed_password: str) -> str:
    """Verify password hashes."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        KeysLoader("keys_config.json").load_jwt_secret_token(),
        algorithm=ALGORITHM,
    )
    return encoded_jwt


def get_password_hash(password: str) -> str:
    """Get hashed password."""
    return pwd_context.hash(password)
