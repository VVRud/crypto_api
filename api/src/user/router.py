from datetime import timedelta

import models
import user.schemas as schemas
from dependencies import session_dependency
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from modules.auth import Auth
from modules.database import Database
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

router = APIRouter(prefix="/user", tags=["User Management"])


@router.post(
    "/create",
    response_model=schemas.User,
    summary="Create user in the database.",
)
async def create_user(
    user: schemas.UserCreation,
    session: AsyncSession = Depends(session_dependency),
    auth: Auth = Depends(Auth.get_auth),
):
    """
    Create user in the database. In case user with the username already exists the error will be returned..
    """
    db_user = await Database.get_user(session, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists.",
        )
    # Create initial user
    db_user = models.User(
        username=user.username, password=auth.get_password_hash(user.password)
    )
    db_user = await Database.create_user(session, db_user)
    return db_user


@router.post(
    "/token", response_model=schemas.Token, summary="Get JWT token for user."
)
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(session_dependency),
    auth: Auth = Depends(Auth.get_auth),
):
    """
    Create JWT Bearer access token for the user. This endpoint requires username and password.
    In case user is not found or password is wrong the error will be raised.
    """
    user = await auth.authenticate_user(
        session, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(
        username=user.username,
        expires_delta=timedelta(minutes=auth.JWT_EXPIRE),
    )
    return {"access_token": access_token, "token_type": "bearer"}
