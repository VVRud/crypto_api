from typing import Annotated

from dependencies import db_session
from fastapi import APIRouter, Depends

# TODO: Change type
db_depends = Annotated[None, Depends(db_session)]
router = APIRouter(prefix="/accounts", tags=["Account Management"])


@router.post("/create")
async def create_account(db_session: db_depends, symbol: str):
    pass


@router.get("/list")
async def list_accounts(db_session: db_depends):
    pass


@router.get("/retrieve")
async def retrieve_account(db_session: db_depends, account_id: int):
    pass
