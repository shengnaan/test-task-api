from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Table


class TableCRUD:
    @staticmethod
    async def create(db: AsyncSession, table_data: dict) -> Table:
        new_table = Table(**table_data)
        db.add(new_table)
        await db.commit()
        await db.refresh(new_table)
        return new_table

    @staticmethod
    async def get_all(db: AsyncSession) -> list[Table]:
        result = await db.execute(select(Table))
        return result.scalars().all()

    @staticmethod
    async def get_by_id(db: AsyncSession, table_id: int) -> Optional[Table]:
        result = await db.execute(
            select(Table).where(Table.id == table_id)
        )
        return result.scalars().first()

    @staticmethod
    async def delete(db: AsyncSession, table_id: int) -> None:
        table = await TableCRUD.get_by_id(db, table_id)
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Столик не найден."
            )
        await db.delete(table)
        await db.commit()
        return
