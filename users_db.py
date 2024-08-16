from sqlalchemy import create_engine, Integer, select, String, insert, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    sessionmaker,
)
from typing import List
import sqlalchemy as sa
from db_base import Base, pg_engine
class User_Info(Base):
    """Go away pep8."""

    __tablename__ = "user_info"

    ids: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    card_number: Mapped[str] = mapped_column(String(255))
    scc: Mapped[int] = mapped_column(Integer)
    card_name: Mapped[str] = mapped_column(String(255))
    expire_date: Mapped[str] = mapped_column(String(255))

    orders: Mapped[List["Order"]] = relationship(
        "Order", back_populates="orders", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        username: str,
        password: str,
        card_number: str,
        scc: int,
        card_name: str,
        expire_date: str,
        ids: int = None,
    ):
        self.username = username
        self.password = password
        self.card_number = card_number
        self.scc = scc
        self.card_name = card_name
        self.expire_date = expire_date
        self.ids = ids


class Users:
    """."""

    def __init__(self):
        self.Session = sessionmaker(bind=pg_engine)
        Base.metadata.create_all(pg_engine)

    def add_user(self, user: User_Info):
        session = self.Session()
        session.add(user)
        session.commit()

