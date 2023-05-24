from pydantic import BaseModel


class Account(BaseModel):
    """Wallet account."""

    id: int
    """Account unique id."""

    name: str
    """Unique account name. If not specified will be randomly generated."""

    class Config:
        orm_mode = True
