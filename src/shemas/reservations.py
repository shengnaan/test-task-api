from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class ReservationBase(BaseModel):
    customer_name: str = Field(..., description="Имя человека оставившего бронь", max_length=100)
    table_id: int = Field(..., description="ID стола")
    reservation_time: datetime = Field(..., description="Время, на которое забронирован столик")
    duration_minutes: int = Field(..., description="Продолжительность брони", ge=30)

    @field_validator("reservation_time")
    def make_naive(cls, value: datetime) -> datetime:
        # Конкретики, касательно времени нет, поэтому все хранится как время без указания таймзоны
        if value.tzinfo is not None and value.utcoffset() is not None:
            value = value.replace(tzinfo=None)
        return value

class ReservationCreate(ReservationBase):
    pass


class ReservationModel(ReservationBase):
    id: int

    class Config:
        from_attributes = True
