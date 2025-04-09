from datetime import timedelta
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import literal_column, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Reservation, Table


class ReservationCRUD:
    @staticmethod
    async def create(db: AsyncSession, reservation_data: dict) -> Reservation:
        result = await db.execute(
            select(Table).where(Table.id == reservation_data.pop("table_id"))
        )
        table = result.scalars().first()
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Столика с таким ID нет."
            )

        new_reservation = Reservation(**reservation_data, table_id=table.id)
        new_reservation.reservation_time = new_reservation.reservation_time.replace(tzinfo=None)
        start_time = new_reservation.reservation_time
        end_time = start_time + timedelta(minutes=new_reservation.duration_minutes)

        stmt = select(Reservation).where(
            Reservation.table_id == new_reservation.table_id,
            Reservation.reservation_time < end_time,
            (Reservation.reservation_time + literal_column(
                "interval '1 minute'") * Reservation.duration_minutes) > start_time
        )
        result = await db.execute(stmt)
        conflict = result.scalars().first()

        if conflict:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Столик уже забронирован в указанный интервал времени."
            )

        db.add(new_reservation)
        await db.commit()
        await db.refresh(new_reservation)
        return new_reservation

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Reservation]:
        result = await db.execute(select(Reservation))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, reservation_id: int) -> Optional[Reservation]:
        result = await db.execute(
            select(Reservation).where(Reservation.id == reservation_id)
        )
        return result.scalars().first()

    @staticmethod
    async def delete(db: AsyncSession, reservation_id: int) -> None:
        reservation = await ReservationCRUD.get_by_id(db, reservation_id)
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бронь не найдена."
            )
        await db.delete(reservation)
        await db.commit()
        return
