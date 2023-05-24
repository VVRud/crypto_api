import os
from typing import Tuple

import pytest
import pytest_asyncio
from models import Account, Address, User
from modules.auth import Auth
from modules.database import Database
from modules.wallet import Wallet
from sqlalchemy_utils import drop_database


@pytest.fixture(scope="session")
def wallet() -> Wallet:
    return Wallet.get_wallet()


@pytest.fixture(scope="session")
def auth() -> Auth:
    return Auth()


@pytest.fixture(scope="function")
def user():
    return User(username="uname", password=Auth().get_password_hash("12345678"))


@pytest.fixture(scope="function")
def account(user: User, wallet: Wallet) -> Account:
    return Account(
        name="acc_name",
        mnemonic=wallet.generate_mnemonic(),
        passphrase=wallet.generate_passphrase(),
        user=user,
    )


@pytest.fixture(scope="function")
def address(account: Account, wallet: Wallet):
    return Address(
        network="BTC",
        address=wallet.generate_address("BTC", account),
        account=account,
    )


@pytest_asyncio.fixture(scope="function")
async def database(address: Address, account, user, request) -> Database:
    db_url = "sqlite+aiosqlite:///./test.db"
    db = Database(db_url)
    try:
        await db.initialize()
        async with db.session_maker() as sess:
            sess.add(address)
            await sess.commit()
            await sess.refresh(address)
            await sess.refresh(account)
            await sess.refresh(user)

        yield db
    finally:
        db.engine.dispose(close=True)
        drop_database(db_url)
