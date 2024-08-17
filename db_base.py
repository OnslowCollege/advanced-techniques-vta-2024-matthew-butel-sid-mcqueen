from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

pg_engine = create_engine(
    "postgresql://postgres:123456@localhost:5432/postgres"
)


class Base(DeclarativeBase):
    """Go away pep8."""

    pass
