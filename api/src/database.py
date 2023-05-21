from models import Base, User
from schemas import UserPassword
from singleton import SingletonMeta
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)


class Database(metaclass=SingletonMeta):
    """Database CRUD class."""

    def __init__(self, connection_string: str):
        self.engine = create_async_engine(connection_string)
        self.session_maker = async_sessionmaker(self.engine, expire_on_commit=False)

    async def initialize_db(self):
        """Create data tables if needed on startup."""
        async with self.engine.begin() as conn:  # type: AsyncConnection
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async def with_session(self):
        """Dependency for session management in functions."""
        async with self.session_maker() as sess:
            yield sess

    @staticmethod
    async def create_user(sess: AsyncSession, user: UserPassword):
        """Create user by its username and password."""
        db_user = User(
            username=user.username, password=user.password, mnemonic="NO mnemonic"
        )
        sess.add(db_user)
        await sess.commit()
        await sess.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user(sess: AsyncSession, username: str):
        """Return user from the database."""
        result = await sess.scalars(select(User).where(User.username == username))
        try:
            return result.one()
        except Exception:
            return None


# TODO: Move to constants
database = Database(
    connection_string="postgresql+asyncpg://my_user:password123@localhost/my_database"
)
