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
    joinedload,
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
    cars: Mapped[List["Car"]] = relationship(
        "Car", back_populates="order", cascade="all, delete-orphan"
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


class Orders:
    """."""

    def __init__(self):
        self.Session = sessionmaker(bind=pg_engine)
        Base.metadata.create_all(pg_engine)

    def add_order(self, order: Order):
        session = self.Session()
        session.add(order)
        session.commit()

    def add_order_with_cars(self, order: Order, cars: List[Car]) -> Order:
        with self.Session() as session:
            for car in cars:
                car.order = order
            session.add(order)
            session.flush()
            session.commit()

            # # Refresh the instance to ensure it's up-to-date with the database
            session.refresh(order)

            for car in order.cars:
                session.refresh(car)
                session.expunge(car)

            session.refresh(order.user)
            order.user.hidden_number()
            session.expunge(order.user)

            # Detach the instance from the session
            session.expunge(order)

        return order