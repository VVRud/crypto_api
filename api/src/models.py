import datetime as dt
from typing import List

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    # created_at: Mapped[dt.datetime] = mapped_column(DateTime(), default=lambda: dt.datetime.now())

    accounts: Mapped[List["Account"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    name: Mapped[str] = mapped_column(String(), nullable=False)
    mnemonic: Mapped[str] = mapped_column(String(), nullable=False)
    passphrase: Mapped[str] = mapped_column(String(), nullable=False)
    # created_at: Mapped[dt.datetime] = mapped_column(DateTime(), default=lambda: dt.datetime.now())

    user: Mapped["User"] = relationship(back_populates="accounts")
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="account",
        cascade="all, delete-orphan",  # order_by="created_at"
    )


class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id"))
    network: Mapped[str] = mapped_column(String(), nullable=False)
    address: Mapped[str] = mapped_column(String(), nullable=False)
    # created_at: Mapped[dt.datetime] = mapped_column(DateTime(), default=lambda: dt.datetime.now())

    account: Mapped["Account"] = relationship(back_populates="addresses")
