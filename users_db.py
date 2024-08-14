from sqlalchemy import create_engine, Integer, select, String, insert, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    sessionmaker,
)
import sqlalchemy as sa

pg_engine = create_engine(
    "postgresql://postgres:123456@localhost:5432/postgres"
)


class Base(DeclarativeBase):
    """Go away pep8."""

    pass


Session = sessionmaker(bind=pg_engine)
session = Session()

class User_Info:
    """Go away pep8."""

    def __init__(
        self,
        username: str,
        password: str,
        card_number: str,
        scc: int,
        card_name: int,
        expire_date: int,
    ):
        self.username = username
        self.password = password
        self.card_number = card_number
        self.scc = scc
        self.card_name = card_name
        self.expire_date = expire_date


class Users(Base):
    """."""

    __tablename__ = "user_info"

    ids: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    card_number: Mapped[str] = mapped_column(String(255))
    scc: Mapped[int] = mapped_column(Integer)
    card_name: Mapped[str] = mapped_column(String(255))
    expire_date: Mapped[str] = mapped_column(String(255))

    def add_user(self, user: User_Info):
        session.add(user)
        session.commit()
