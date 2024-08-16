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
from datetime import date


pg_engine = create_engine(
    "postgresql://postgres:123456@localhost:5432/postgres"
)


class Base(DeclarativeBase):
    """Go away pep8."""

    pass


class Order(Base):
    """Go away pep8."""

    __tablename__ = "order"

    id: Mapped[int] = (mapped_column(Integer, primary_key=True),)
    date: Mapped[date] = (mapped_column(Date),)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_info.ids"))

    # Relationship to UserInfo
    user: Mapped["UserInfo"] = relationship(
        "UserInfo", back_populates="orders"
    )

    def __init__(
        self,
        user: User_Info,
        date: date,
        id: int = None,
    ):
        self.date = date
        self.user = user
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

