"""User Database."""
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

    # Relationship to Order
    orders: Mapped["Order"] = relationship("Order", back_populates="user")

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

    def hidden_number(self) -> str:
        """Return the credit card number."""
        return "**** **** **** " + self.card_number[-4:]

class Users:
    """."""

    def __init__(self):
        self.Session = sessionmaker(bind=pg_engine)
        Base.metadata.create_all(pg_engine)

    def get_user(self, user_id: int) -> User_Info:
        user: User_Info

        query = select(User_Info).where(User_Info.ids == user_id)

        with Session(pg_engine) as session:
            user = session.execute(query).scalar_one()
            session.expunge(user)

        return user

    def add_user(self, user: User_Info) -> User_Info:
        with self.Session() as session:
            session.add(user)
            session.flush()  # This assigns the primary key if it's auto-generated
            session.commit()

            # Refresh the instance to ensure it's up-to-date with the database
            session.refresh(user)

            # Detach the instance from the session
            session.expunge(user)

        return user
