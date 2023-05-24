import pytest
from models import Account, Address, User
from modules.database import Database

from .fixtures import account, address, database, user, wallet


@pytest.mark.asyncio
async def test_user(database: Database, user: User):
    async with database.session_maker() as session:
        u1 = await database.get_user(session, user.username)
        assert (
            user.id == u1.id
            and user.username == u1.username
            and user.password == u1.password
        )

        u2_s = await database.create_user(
            session, User(username="u2", password="rrrrrrr")
        )
        u2_l = await database.get_user(session, "u2")
        assert (
            u2_s.id == u2_l.id
            and u2_s.username == u2_l.username
            and u2_s.password == u2_l.password
        )

        assert await database.get_user(session, "u3") is None

        with pytest.raises(Exception):
            await database.create_user(
                session, User(username="u2", password="rrrrrrr")
            )

        with pytest.raises(Exception):
            await database.create_user(session, User(username="u3"))

        with pytest.raises(Exception):
            await database.create_user(session, User(password="rrrrrrr"))


@pytest.mark.asyncio
async def test_account(database: Database, user: User):
    async with database.session_maker() as session:
        a2_s = Account(name="n1", mnemonic="m1", passphrase="p1")
        a2_s = await database.create_account(session, user, a2_s)

        a1 = await database.get_account_by_name(session, user, a2_s.name)
        assert (
            a2_s.id == a1.id
            and a2_s.mnemonic == a1.mnemonic
            and a2_s.passphrase == a1.passphrase
        )

        a1 = await database.get_account_by_id(session, user, a2_s.id)
        assert (
            a2_s.id == a1.id
            and a2_s.mnemonic == a1.mnemonic
            and a2_s.passphrase == a1.passphrase
        )

        a2_l = await database.get_account_by_id(session, user, a2_s.id)
        a2_n = await database.get_account_by_name(session, user, a2_s.name)
        assert (
            a2_s.id == a2_l.id
            and a2_s.mnemonic == a2_l.mnemonic
            and a2_s.passphrase == a2_l.passphrase
        )
        assert (
            a2_s.id == a2_n.id
            and a2_s.mnemonic == a2_n.mnemonic
            and a2_s.passphrase == a2_n.passphrase
        )

        assert await database.get_account_by_id(session, user, 100) is None

        assert await database.get_account_by_name(session, user, "n100") is None

        with pytest.raises(Exception):
            await database.create_account(
                session,
                user,
                Account(name="n1", mnemonic="m1", passphrase="p1"),
            )

        with pytest.raises(Exception):
            await database.create_account(
                session, user, Account(name="n1", mnemonic="m1")
            )

        with pytest.raises(Exception):
            await database.create_account(
                session, user, Account(name="n1", passphrase="p1")
            )

        with pytest.raises(Exception):
            await database.create_account(
                session, user, Account(mnemonic="m1", passphrase="p1")
            )


@pytest.mark.asyncio
async def test_address(database: Database, account: Account):
    async with database.session_maker() as session:
        a2_s = Address(network="NET1", address="0xVVRud")
        a2_s = await database.create_address(session, account, a2_s)

        a1 = await database.get_address_by_id(session, account, a2_s.id)
        assert (
            a2_s.id == a1.id
            and a2_s.network == a1.network
            and a2_s.address == a1.address
        )

        a1 = await database.get_address_by_network(
            session, account, a2_s.network
        )
        assert (
            a2_s.id == a1.id
            and a2_s.network == a1.network
            and a2_s.address == a1.address
        )

        a2_l = await database.get_address_by_id(session, account, a2_s.id)
        a2_n = await database.get_address_by_network(
            session, account, a2_s.network
        )
        assert (
            a2_s.id == a2_l.id
            and a2_s.network == a2_l.network
            and a2_s.address == a2_l.address
        )
        assert (
            a2_s.id == a2_n.id
            and a2_s.network == a2_n.network
            and a2_s.address == a2_n.address
        )

        assert await database.get_address_by_id(session, account, 100) is None

        assert (
            await database.get_address_by_network(session, account, "n100")
            is None
        )

        with pytest.raises(Exception):
            await database.create_address(
                session, account, Address(network="NET1", address="0xVVRud")
            )

        with pytest.raises(Exception):
            await database.create_address(
                session, account, Address(network="NET1")
            )

        with pytest.raises(Exception):
            await database.create_address(
                session, account, Address(address="0xVVRud")
            )
