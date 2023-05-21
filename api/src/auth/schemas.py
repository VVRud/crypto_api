from pydantic import BaseModel


class Token(BaseModel):
    """Access token for an API. Bound to a user."""

    access_token: str
    token_type: str
