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
    return [TableModel.model_validate(obj) for obj in await TableCRUD.get_all(db)]


@table_router.post(
    "/",
    response_model=TableModel,
    status_code=status.HTTP_201_CREATED
)
async def create_table(
    table_data: TableCreate,
    db: AsyncSession = Depends(get_db),
) -> TableModel:
    return TableModel.model_validate(await TableCRUD.create(db, table_data.dict()))


@table_router.delete(
    "/{table_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_table(
    table_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    await TableCRUD.delete(db, table_id)
