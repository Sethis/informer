from aiogram import Router

from src.presentation.routers.service import starting
from src.presentation.routers import information, admin

common_router = Router()

common_router.include_routers(
    starting.router,
    information.start.router,
    admin.start.router,
    information.dialog.dialog,
    admin.dialog.dialog
)
