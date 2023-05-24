from pydantic import BaseModel


class Address(BaseModel):
    """"""

    id: int
    """Unique integer identifier."""

    network: str
    """Network of the address."""

    address: str
    """Address."""

    class Config:
        orm_mode = True
