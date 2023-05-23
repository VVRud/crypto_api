from pydantic import BaseModel, Field


class Token(BaseModel):
    """Access token for an API. Bound to a user."""

    access_token: str
    token_type: str


class UserBase(BaseModel):
    """Basic user class"""

    username: str
    """Unique username."""


class UserCreation(UserBase):
    """Model for user creation."""

    password: str = Field(min_length=8)
    """Strong password."""


class User(UserBase):
    """User model."""

    id: int
    """Unique user id."""

    class Config:
        orm_mode = True
