from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    mnemonic: Mapped[str] = mapped_column(String(), nullable=False)

    accounts: Mapped[List["Account"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"User({self.username}, {self.password}, {self.mnemonic}, {self.accounts})"
        )


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    network: Mapped[str] = mapped_column(String(), nullable=False)
    passphrase: Mapped[str] = mapped_column(String(), nullable=True)

    user: Mapped["User"] = relationship(back_populates="accounts")
