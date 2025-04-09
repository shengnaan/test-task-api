from datetime import datetime, timedelta

from sqlalchemy import (
    Column,
    ColumnElement,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    String,
    text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
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
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)

    table = relationship("Table", backref="reservations")

    @hybrid_property
    def end_time(self) -> datetime:
        """Гибридный метод, который избавляет от лишних строк при работе на уровне python"""
        return self.reservation_time + timedelta(minutes=self.duration_minutes)

    @end_time.expression
    def end_time(cls) -> ColumnElement:
        """Аналогично с предыдущим, только вызывается, когда происходят SQL запросы"""
        return cls.reservation_time + (cls.duration_minutes * text("'1 minute'::interval"))
