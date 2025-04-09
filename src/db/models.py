from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base(metadata=MetaData())


class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    seats = Column(Integer, nullable=False)
    location = Column(String, nullable=False)


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String, nullable=False)
    table_id = Column(Integer, ForeignKey("tables.id"), nullable=False)
    reservation_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    duration_minutes = Column(Integer, nullable=False)

    table = relationship("Table", backref="reservations")
