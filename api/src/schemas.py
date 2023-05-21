from pydantic import BaseModel, Field


class UserBase(BaseModel):
    username: str
    """Unique username slug."""


class UserPassword(UserBase):
    """Model for user creation."""

    password: str = Field(min_length=8)
    """Strong password"""


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
