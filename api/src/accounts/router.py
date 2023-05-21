from typing import Annotated

from dependencies import db_session
from fastapi import APIRouter, Depends

# TODO: Change type
db_depends = Annotated[None, Depends(db_session)]
router = APIRouter(prefix="/accounts", tags=["Account Management"])


@router.post("/create")
async def create_account(symbol: str):
    """Docs here."""
    pass


@router.get("/list")
async def list_accounts(db_session: db_depends):
    """Docs here."""
    pass


@router.get("/retrieve")
async def retrieve_account(account_id: int):
    """Docs here."""
    pass
