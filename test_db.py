"""OKOKOKOK."""

from sqlalchemy import create_engine, Integer, select, String, insert, MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
)
import sqlalchemy as sa

pg_engine = create_engine(
    "postgresql://postgres:123456@localhost:5432/postgres"
)

class Base(DeclarativeBase):
    """Go away pep8."""

    pass

class User_Info(Base):
    """Go away pep8."""

    __tablename__ = "user_info"

    username: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
    card_number: Mapped[int] = mapped_column(Integer)
    scc: Mapped[int] = mapped_column(Integer)
    card_name: Mapped[str] = mapped_column(String(255))
    expire_date: Mapped[int] = mapped_column(Integer)

user1 = User_Info()


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

    # def __repr__(self) -> str:
    #    """Go away pep8."""
    #    return f"{self.make} {self.model} {self.year_made}"

    def __repr__(self) -> str:
        """Go away pep8."""
        return f"{self.ids}, {self.transmission}, {self.make}, {self.model}, {self.year_made, self.mileage, self.price}"


Base.metadata.create_all(pg_engine)

query = select(Cars)
cars_transmission: list[str] = []
cars_make: list[str] = []
cars_model: list[str] = []
cars_year_made: list[str] = []
cars_info: str = ""
cars_help: list[str] = []
with Session(pg_engine) as session:
    result = session.execute(query)
    for row in result:
        if row != "":
            cars_info = row[0]
            print(cars_info.ids)
            print(cars_info.transmission)
            print(cars_info.make)
            print(cars_info.model)
            print(cars_info.year_made)
            print(cars_info.mileage)
            print(cars_info.price)
            cars_help = str(cars_info).split(", ")

test_inserting = insert(user_info).values(
    username="Matthew",
    password="MB",
    card_number=1234,
    scc=333,
    card_name="Matthew",
    expire_date=23,
)