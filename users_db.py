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


class User_Info(Base):
    """Go away pep8."""

    __tablename__ = "user_info"

    ids: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    card_number: Mapped[int] = mapped_column(Integer)
    scc: Mapped[int] = mapped_column(Integer)
    card_name: Mapped[str] = mapped_column(String(255))
    expire_date: Mapped[int] = mapped_column(Integer)


user1 = User_Info(
    username="Matthew",
    password="Mattheww",
    card_number=123456,
    scc=123,
    card_name="Matthewww",
    expire_date=12,
)
session.add(user1)

session.commit()
