import models
from address import schemas
from dependencies import oauth2_scheme_dependency, session_dependency
from fastapi import APIRouter, Depends, HTTPException, Query
from modules.auth import Auth
from modules.database import Database
from modules.wallet import Wallet
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

router = APIRouter(prefix="/address", tags=["Addresses Management"])


@router.post(
    "/create",
    response_model=schemas.Address,
    summary="Create address for an account.",
)
async def create_address(
    token: str = Depends(oauth2_scheme_dependency),
    network: str = Query(
        default="ETH",
        description="Network symbol you want to generate address for.",
    ),
    account_id: int = Query(
        ..., description="Account id you want to generate your address for."
    ),
    auth: Auth = Depends(Auth.get_auth),
    wallet: Wallet = Depends(Wallet.get_wallet),
    session: AsyncSession = Depends(session_dependency),
):
    """
    Create address for an account id in network that provided.
    If address exist for the provided network, an error will be raised.
    """
    user = await auth.get_current_user(session, token)
    wallet.validate_symbol(network)
    account = await Database.get_account_by_id(session, user, account_id)
    if (
        await Database.get_address_by_network(session, account, network)
    ) is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Address on this network already exists.",
        )

    address = models.Address(
        network=network, address=wallet.generate_address(network, account)
    )
    address = await Database.create_address(session, account, address)
    return address


@router.get(
    "/list",
    response_model=list[schemas.Address],
    summary="List existing addresses for an account.",
)
async def list_addresses(
    token: str = Depends(oauth2_scheme_dependency),
    account_id: int = Query(..., description="Account id you want to list."),
    auth: Auth = Depends(Auth.get_auth),
    session: AsyncSession = Depends(session_dependency),
):
    """Retrieve and list account addresses."""
    user = await auth.get_current_user(session, token)
    account = await Database.get_account_by_id(session, user, account_id)
    return await account.awaitable_attrs.addresses


@router.get(
    "/retrieve",
    response_model=None | schemas.Address,
    summary="Retrieve particular address.",
)
async def retrieve_address(
    token: str = Depends(oauth2_scheme_dependency),
    account_id: int = Query(
        ..., description="Account id you want to retrieve your address from."
    ),
    address_id: int = Query(
        ..., description="Address id you want to retrieve."
    ),
    auth: Auth = Depends(Auth.get_auth),
    session: AsyncSession = Depends(session_dependency),
):
    """Return address by an id from an account. if address does not exist null will be returned."""
    user = await auth.get_current_user(session, token)
    account = await Database.get_account_by_id(session, user, account_id)
    address = await Database.get_address_by_id(session, account, address_id)
    return address
