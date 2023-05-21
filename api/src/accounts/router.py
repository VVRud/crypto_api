from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import database

# TODO: Change type
router = APIRouter(prefix="/accounts", tags=["Account Management"])


@router.post("/create")
async def create_account(
    symbol: str, session: AsyncSession = Depends(database.with_session)
):
    """Docs here."""
    pass


@router.get("/list")
async def list_accounts(session: AsyncSession = Depends(database.with_session)):
    """Docs here."""
    pass


@router.get("/retrieve")
async def retrieve_account(
    account_id: int, session: AsyncSession = Depends(database.with_session)
):
    """Docs here."""
    pass
