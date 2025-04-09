from fastapi import APIRouter

from core.config import Settings
from src.routers.v1.reservations import reservation_router
from src.routers.v1.tables import table_router

base_router = APIRouter(prefix=Settings.API_VERSION)

base_router.include_router(table_router)
base_router.include_router(reservation_router)
