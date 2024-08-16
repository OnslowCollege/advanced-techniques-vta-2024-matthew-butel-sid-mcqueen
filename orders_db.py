from sqlalchemy import (
    create_engine,
    Integer,
    select,
    String,
    insert,
    Date,
    MetaData,
    ForeignKey,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    Session,
    sessionmaker,
)
import sqlalchemy as sa
from users_db import User_Info
from cars_db import Car
from datetime import date
from typing import List
from db_base import Base, pg_engine

class Order(Base):
    """Go away pep8."""

    __tablename__ = "order"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    date: Mapped[date] = mapped_column(Date)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_info.ids"))
    total_price: Mapped[int] = mapped_column(Integer)

    # Relationship to UserInfo
    user: Mapped["User_Info"] = relationship(
        "User_Info", back_populates="orders"
    )

    # Relationship to Order_Car
    order_cars: Mapped[List["Order_Car"]] = relationship(
        "Order_Car", back_populates="order", cascade="all, delete-orphan"
    )

    def __init__(
        self,
        user: User_Info,
        date: date,
        total_price: int,
        id: int = None,
    ):
        self.date = date
        self.user = user
        self.total_price = total_price
        self.id = id


class Order_Car(Base):
    """Go away pep8."""

    __tablename__ = "order_car"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"))
    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("car.ids"))

    order: Mapped["Order"] = relationship("Order", back_populates="order_cars")
    car: Mapped["Car"] = relationship("Car", back_populates="order_cars")

    def __init__(
        self,
        order: Order,
        car: Car,
        id: int = None,
    ):
        self.order = order
        self.car = car
        self.id = id


class Orders:
    """."""

    def __init__(self):
        self.Session = sessionmaker(bind=pg_engine)
        Base.metadata.create_all(pg_engine)

    def add_order(self, order: Order):
        session = self.Session()
        session.add(order)
        session.commit()

    def add_order_with_cars(self, order: Order, cars: List[Car]):
        session = self.Session()
        for car in cars:
            order_car = Order_Car(order=order, car=car)
            order.order_cars.append(order_car)
        session.add(order)
        session.commit()