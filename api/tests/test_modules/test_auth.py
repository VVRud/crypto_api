import pytest
from fastapi import HTTPException
from models import User
from modules.auth import Auth
from modules.database import Database


def test_password_verification(auth: Auth):
    pwd = "12345678"
    hashed = auth.get_password_hash(pwd)
    assert hashed != pwd
    assert hashed != auth.get_password_hash(pwd)
    assert auth.verify_password(pwd, hashed)
    assert not auth.verify_password(hashed, hashed)


@pytest.mark.asyncio
async def test_user_authentication(auth: Auth, database: Database, user: User):
    async with database.session_maker() as session:
        u = await auth.authenticate_user(session, "random", "random")
        assert u is None

        u = await auth.authenticate_user(session, user.username, "random")
        assert u is None

        u = await auth.authenticate_user(session, user.username, user.password)
        assert u == u


@pytest.mark.asyncio
@pytest.mark.parametrize("username", (None, "random"))
async def test_user_jwt_fails(auth: Auth, database: Database, username):
    t1 = auth.create_access_token(username)
    assert t1 is not None

    async with database.session_maker() as session:
        with pytest.raises(HTTPException) as e:
            await auth.get_current_user(session, t1)
            assert e.value.detail == "Could not validate credentials"


@pytest.mark.asyncio
async def test_user_jwt_succeeds(auth: Auth, database: Database, user: User):
    t1 = auth.create_access_token(user.username)
    assert t1 is not None

    async with database.session_maker() as session:
        u = await auth.get_current_user(session, t1)
        assert u == u
