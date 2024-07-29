"""OKOKOKOK."""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import Base

pg_engine = create_engine(
    "posthgresql://postgres:123456@localhost:5432/postgres"
)


class Cars(Base):
    """Go away pep8."""

    __tablename__ = "cars"

    transmission: Mapped[str] = mapped_column(str(255))
    make: Mapped[str] = mapped_column(str(255))
