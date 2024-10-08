"""Car database."""

from sqlalchemy import (
    create_engine,
    Integer,
    select,
    String,
    or_,
    and_,
    ForeignKey,
    func,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    sessionmaker,
)
from db_base import Base, pg_engine
from typing import List, Optional


class Car(Base):
    __tablename__ = "cars"

    ids: Mapped[int] = mapped_column(Integer, primary_key=True)
    transmission: Mapped[str] = mapped_column(String(255))
    make: Mapped[str] = mapped_column(String(255))
    model: Mapped[str] = mapped_column(String(255))
    year_made: Mapped[str] = mapped_column(String(255))
    mileage: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    order_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("order.id"), nullable=True
    )

    order: Mapped["Order"] = relationship("Order", back_populates="cars")

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

class Cars:
    """Go away pep8."""

    def __init__(self):
        self.Session = sessionmaker(bind=pg_engine)
        Base.metadata.create_all(pg_engine)

    def get_cars(self, transmission: str, make: str) -> list[Car]:
        """."""
        cars = []

        query = select(Car).where(
            and_(
                func.coalesce(Car.order_id, 0) == 0,
                or_(transmission == "All", Car.transmission == transmission),
                or_(make == "All", Car.make == make),
            )
        )

        """Retrieve all cars from the database."""
        with Session(pg_engine) as session:
            result = session.execute(query)
            for row in result:
                if row != "":
                    cars_info = row[0]
                    cars.append(cars_info)

        return cars