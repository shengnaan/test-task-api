from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.connection import get_db
from src.repositories.tables import TableCRUD
from src.shemas.tables import TableCreate, TableModel

table_router = APIRouter(
    prefix="/tables",
    tags=["Tables"]
)


@table_router.get(
    "/",
    response_model=list[TableModel]
)
async def get_tables(
    db: AsyncSession = Depends(get_db),
) -> list[TableModel]:
    tables = await TableCRUD.get_all(db)
    return tables


@table_router.post(
    "/",
    response_model=TableModel,
    status_code=status.HTTP_201_CREATED
)
async def create_table(
    table_data: TableCreate,
    db: AsyncSession = Depends(get_db),
) -> TableModel:
    table = await TableCRUD.create(db, table_data.dict())
    return table


@table_router.delete(
    "/{table_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_table(
    table_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    await TableCRUD.delete(db, table_id)
