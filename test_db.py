"""OKOKOKOK."""

from sqlalchemy import create_engine, Integer, select, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)

pg_engine = create_engine(
    "postgresql://postgres:123456@localhost:5432/postgres"
)
pg_engine.connect()

class Base(DeclarativeBase):
    pass

class Cars(Base):
    """Go away pep8."""

    __tablename__ = "cars"

    ids: Mapped[int] = mapped_column(Integer, primary_key=True)
    transmission: Mapped[str] = mapped_column(String(255))
    make: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    year_made: Mapped[str] = mapped_column(String(255))
    mileage: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)

Base.metadata.create_all(pg_engine)

query = select(Cars)
