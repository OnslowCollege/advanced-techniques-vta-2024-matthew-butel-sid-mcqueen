"""OKOKOKOK."""

from sqlalchemy import create_engine

engine = create_engine("postgrespl+pypostgrespl:///:memory:", echo=True)
