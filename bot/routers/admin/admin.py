from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup as RKeyboard, KeyboardButton as RButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.routers.admin import statistic_router, newsletter_router, channel_router, utm_router
from bot.states.admin_st import AdminSt
from bot.vars import bot
from config import ADMINS

admin_router = Router(name="AdminRouter")
# Filters
admin_router.message.filter(F.from_user.id.in_(ADMINS))
# Including Sub Routers
admin_router.include_routers(
    statistic_router,
    newsletter_router,
    channel_router,
    utm_router
)


@admin_router.message(Command("admin"))
async def admin_handler(message: types.Message, state: FSMContext):
    keyboard = RKeyboard(resize_keyboard=True, keyboard=[
        [RButton(text="Статистика"), RButton(text="Рассылка")],
        [RButton(text="UTM-Метки"), RButton(text="Каналы")],
    ])

    await bot.send_message(
        message.chat.id,
        "<b>Админ панель</b>",
        reply_markup=keyboard
    )

    await state.set_state(AdminSt.MENU)
