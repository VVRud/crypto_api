from datetime import timedelta

from auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES
from auth.schemas import Token
from auth.utils import authenticate_user, create_access_token, get_password_hash
from fastapi import APIRouter, Depends, HTTPException
from schemas import User, UserPassword
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import database

router = APIRouter(prefix="/user", tags=["User Management."])


@router.post("/create", response_model=User, summary="Create user in the database.")
async def create_user(
    user: UserPassword, session: AsyncSession = Depends(database.with_session)
):
    """Docs here."""
    db_user = await database.get_user(session, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists."
        )
    # TODO: add mnemonic
    user.password = get_password_hash(user.password)
    db_user = await database.create_user(session, user)
    return db_user


@router.post("/token", response_model=Token, summary="Get JWT token for user.")
async def login_for_access_token(
    user: UserPassword, session: AsyncSession = Depends(database.with_session)
):
    """Docs here."""
    user = await authenticate_user(session, user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}
