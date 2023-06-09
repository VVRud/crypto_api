import models
from account import schemas
from dependencies import oauth2_scheme_dependency, session_dependency
from fastapi import APIRouter, Depends, HTTPException, Query
from modules.auth import Auth
from modules.database import Database
from modules.wallet import Wallet
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

router = APIRouter(prefix="/account", tags=["Accounts Management"])


@router.post(
    "/create",
    response_model=schemas.Account,
    summary="Create an account for a user.",
)
async def create_account(
    name: None
    | str = Query(
        default=None,
        description="Unique account name. If not specified will be randomly generated.",
    ),
    token: str = Depends(oauth2_scheme_dependency),
    auth: Auth = Depends(Auth.get_auth),
    wallet: Wallet = Depends(Wallet.get_wallet),
    session: AsyncSession = Depends(session_dependency),
):
    """
    Create an account for a user. In case name is not provided it will be randomly generated.
    If an account name exists for a user, an error will be raised.
    """
    user = await auth.get_current_user(session, token)
    if name is None:
        name = "-".join(
            wallet.encoder.decrypt(wallet.generate_mnemonic()).split(" ")[:2]
        )
    elif (await Database.get_account_by_name(session, user, name)) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account with this name already exists.",
        )
    account = models.Account(
        name=name,
        mnemonic=wallet.generate_mnemonic(),
        passphrase=wallet.generate_passphrase(),
    )
    account = await Database.create_account(session, user, account)
    return account


@router.get(
    "/list", response_model=list[schemas.Account], summary="List user accounts."
)
async def list_accounts(
    token: str = Depends(oauth2_scheme_dependency),
    auth: Auth = Depends(Auth.get_auth),
    session: AsyncSession = Depends(session_dependency),
):
    """Get all user existing accounts."""
    user = await auth.get_current_user(session, token)
    return await user.awaitable_attrs.accounts


@router.get(
    "/retrieve",
    response_model=None | schemas.Account,
    summary="Retrieve an account.",
)
async def retrieve_account(
    account_id: int = Query(
        ..., title="Account ID.", description="Unique account ID."
    ),
    token: str = Depends(oauth2_scheme_dependency),
    auth: Auth = Depends(Auth.get_auth),
    session: AsyncSession = Depends(session_dependency),
):
    """Retrieve user account by its id. If account does not exist, null will be returned."""
    user = await auth.get_current_user(session, token)
    return await Database.get_account_by_id(session, user, account_id)
