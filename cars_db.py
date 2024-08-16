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

class Car:
    def __init__(self, transmission: str, make: str, model: str, year_made: str, mileage: int, price: int, ids: int = None):
        self.ids = ids
        self.transmission = transmission
        self.make = make
        self.model = model
        self.year_made = year_made
        self.mileage = mileage
        self.price = price

    def __repr__(self) -> str:
        return f"{self.make} {self.model} {self.year_made}"

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

    def __repr__(self) -> str:
        """Go away pep8."""
        return f"{self.make} {self.model} {self.year_made}"

    def get_cars(self, transmission: str) -> list[Car]:
        """."""
        Base.metadata.create_all(pg_engine)
        cars = []

        query = select(Cars).where(
            transmission == "All" or Cars.transmission == transmission
        )

        """Retrieve all cars from the database."""
        with Session(pg_engine) as session:
            result = session.execute(query)
            for row in result:
                if row != "":
                    cars_info = row[0]
                    car = Car(
                        transmission=cars_info.transmission,
                        make=cars_info.make,
                        model=cars_info.model,
                        year_made=cars_info.year_made,
                        mileage=cars_info.mileage,
                        price=cars_info.price
                    )
                    cars.append(car)

        return cars



#Base.metadata.create_all(pg_engine)
#query = select(Cars)

#with Session(pg_engine) as session:
#    result = session.execute(query)
#    for row in result:
#        print(row)