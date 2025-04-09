from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Reservation
from src.repositories.tables import TableCRUD


class ReservationCRUD:
    @staticmethod
    async def create(db: AsyncSession, data: dict) -> Reservation:
        if not await TableCRUD.get_by_id(db, data["table_id"]):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Столика с таким ID нет."
            )

        reservation = Reservation(**data)

        overlapping_stmt = (
            select(Reservation)
            .where(
                Reservation.table_id == data["table_id"],
                Reservation.reservation_time < reservation.end_time,
                Reservation.end_time > reservation.reservation_time
            )
        )

        existing = await db.scalar(overlapping_stmt)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Столик уже забронирован в указанный интервал времени."
            )

        db.add(reservation)
        await db.commit()
        await db.refresh(reservation)
        return reservation

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
