from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.connection import get_db
from src.repositories.reservations import ReservationCRUD
from src.shemas.reservations import ReservationCreate, ReservationModel

reservation_router = APIRouter(
    prefix="/reservations",
    tags=["Reservations"]
)


@reservation_router.get(
    "/",
    response_model=list[ReservationModel]
)
async def get_reservations(
    db: AsyncSession = Depends(get_db),
) -> list[ReservationModel]:
    return [
        ReservationModel.model_validate(obj) for obj in await ReservationCRUD.get_all(db)
    ]


@reservation_router.post(
    "/",
    response_model=ReservationModel,
    status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    reservation_data: ReservationCreate,
    db: AsyncSession = Depends(get_db),
) -> ReservationModel:
    return ReservationModel.model_validate(
        await ReservationCRUD.create(db, reservation_data.dict())
    )


@reservation_router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_reservation(
    reservation_id: int,
    db: AsyncSession = Depends(get_db),
) -> None:
    await ReservationCRUD.delete(db, reservation_id)
