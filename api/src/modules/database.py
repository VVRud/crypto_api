import config
import models
from modules.singleton import Singleton
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database(Singleton):
    """Database CRUD class."""

    CONNECTION_STRING = config.DATABASE_CONNECTION_STRING

    def __init__(self):
        self.engine = create_async_engine(self.CONNECTION_STRING)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    @classmethod
    def get_database(cls) -> "Database":
        """Get database connection."""
        return cls()

    async def initialize(self):
        """Create data tables if needed on startup."""
        async with self.engine.begin() as conn:  # type: AsyncConnection
            await conn.run_sync(models.Base.metadata.create_all, checkfirst=True)

    @staticmethod
    async def create_user(sess: AsyncSession, user: models.User):
        """Create user by its username and password."""
        sess.add(user)
        await sess.commit()
        await sess.refresh(user)
        return user

    @staticmethod
    async def get_user(sess: AsyncSession, username: str):
        """Return user from the database."""
        stmt = select(models.User).where(models.User.username == username)
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def create_account(
        sess: AsyncSession, user: models.User, account: models.Account
    ):
        account.user = user
        sess.add(account)
        await sess.commit()
        await sess.refresh(account)
        return account

    @staticmethod
    async def get_account_by_id(
        sess: AsyncSession, user: models.User, account_id: int
    ) -> None | models.Account:
        stmt = select(models.Account).where(
            models.Account.id == account_id and models.Account.user == user
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def get_account_by_name(
        sess: AsyncSession, user: models.User, name: str
    ) -> None | models.Account:
        stmt = select(models.Account).where(
            models.Account.name == name and models.Account.user == user
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def create_address(
        sess: AsyncSession, account: models.Account, address: models.Address
    ):
        """Create user by its username and password."""
        address.account = account
        sess.add(address)
        await sess.commit()
        await sess.refresh(address)
        return address

    @staticmethod
    async def get_address_by_id(
        sess: AsyncSession, account: models.Account, address_id: int
    ):
        stmt = select(models.Address).where(
            models.Address.id == address_id and models.Address.account == account
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def get_address_by_network(
        sess: AsyncSession, account: models.Account, network: str
    ) -> None | models.Account:
        stmt = select(models.Address).where(
            models.Address.network == network and models.Address.account == account
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()
