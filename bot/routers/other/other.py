from aiogram import Router

from bot.routers.other import back_router

other_router = Router(name="OtherRouter")
# Including Sub Routers
other_router.include_routers(
    back_router
)
