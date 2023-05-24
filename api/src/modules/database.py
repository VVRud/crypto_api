import config
import models
from fastapi import HTTPException
from modules.singleton import Singleton
from sqlalchemy import URL, select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from starlette import status


class Database(Singleton):
    """Database CRUD class."""

    def __init__(self, conn_string: str | URL):
        self.engine = create_async_engine(conn_string)
        self.session_maker = async_sessionmaker(
            self.engine, expire_on_commit=False
        )

    @classmethod
    def get_database(cls) -> "Database":
        """Get database connection context."""
        return cls(config.DATABASE_CONNECTION_STRING)

    async def initialize(self):
        """Create data tables if needed on startup."""
        async with self.engine.begin() as conn:  # type: AsyncConnection
            await conn.run_sync(
                models.Base.metadata.create_all, checkfirst=True
            )

    @staticmethod
    async def create_user(sess: AsyncSession, user: models.User) -> models.User:
        """Create user by its username and password."""
        sess.add(user)
        await sess.commit()
        await sess.refresh(user)
        return user

    @staticmethod
    async def get_user(sess: AsyncSession, username: str) -> None | models.User:
        """Return user from the database."""
        stmt = select(models.User).where(models.User.username == username)
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def create_account(
        sess: AsyncSession, user: models.User, account: models.Account
    ) -> models.Account:
        """Create account for a user."""
        if (
            await Database.get_account_by_name(sess, user, account.name)
        ) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account with this name already exists.",
            )
        account.user = user
        sess.add(account)
        await sess.commit()
        await sess.refresh(account)
        return account

    @staticmethod
    async def get_account_by_id(
        sess: AsyncSession, user: models.User, account_id: int
    ) -> None | models.Account:
        """Get account for user by its id."""
        stmt = select(models.Account).where(
            models.Account.id == account_id and models.Account.user == user
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def get_account_by_name(
        sess: AsyncSession, user: models.User, name: str
    ) -> None | models.Account:
        """Get account by its name."""
        stmt = select(models.Account).where(
            models.Account.name == name and models.Account.user == user
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def create_address(
        sess: AsyncSession, account: models.Account, address: models.Address
    ) -> models.Address:
        """Create address for an account."""
        if (
            await Database.get_address_by_network(
                sess, account, address.network
            )
        ) is not None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Address on this network already exists.",
            )
        address.account = account
        sess.add(address)
        await sess.commit()
        await sess.refresh(address)
        return address

    @staticmethod
    async def get_address_by_id(
        sess: AsyncSession, account: models.Account, address_id: int
    ) -> None | models.Address:
        """Get address by its id."""
        stmt = select(models.Address).where(
            models.Address.id == address_id
            and models.Address.account == account
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()

    @staticmethod
    async def get_address_by_network(
        sess: AsyncSession, account: models.Account, network: str
    ) -> None | models.Address:
        """Get address by its network."""
        stmt = select(models.Address).where(
            models.Address.network == network
            and models.Address.account == account
        )
        result = await sess.scalars(stmt)
        return result.one_or_none()
