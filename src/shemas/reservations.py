from datetime import datetime

from pydantic import BaseModel, Field


class ReservationBase(BaseModel):
    customer_name: str = Field(..., description="Имя человека оставившего бронь", max_length=100)
    table_id: int = Field(..., description="ID стола")
    reservation_time: datetime = Field(..., description="Время, на которое забронирован столик")
    duration_minutes: int = Field(..., description="Продолжительность брони", ge=30)


class ReservationCreate(ReservationBase):
    pass


class ReservationModel(ReservationBase):
    id: int

    class Config:
        orm_mode = True
