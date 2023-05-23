from pydantic import BaseModel


class Address(BaseModel):
    """"""

    id: int

    network: str

    address: str

    class Config:
        orm_mode = True
