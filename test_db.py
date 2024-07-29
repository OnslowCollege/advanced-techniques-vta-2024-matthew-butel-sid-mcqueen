"""OKOKOKOK."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Base

pg_engine = create_engine(
    "posthgresql://postgres:123456@localhost:5432/postgres"
)


class Cars(Base):
    __tablename__ = "cars"
