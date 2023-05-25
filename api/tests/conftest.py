import pytest
import pytest_asyncio
from dependencies import session_dependency
from httpx import AsyncClient
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


@pytest_asyncio.fixture(scope="function")
async def client(database) -> AsyncClient:
    from main import app

    async def override_session_dependency():
        async with database.session_maker() as session:
            yield session

    app.dependency_overrides[session_dependency] = override_session_dependency

    client = AsyncClient(app=app, base_url="http://test")
    yield client
    await client.aclose()


@pytest_asyncio.fixture(scope="function")
async def token(client, user) -> str:
    response = await client.post(
        f"/user/token", data={"username": user.username, "password": "12345678"}
    )

    return response.json()["access_token"]
