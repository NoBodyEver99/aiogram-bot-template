from aiogram import Router, types, F

from bot.states.admin_st import AdminSt
from bot.vars import bot
from db.models import User

statistic_router = Router(name="StatisticRouter")


@statistic_router.message(F.text == "Статистика", AdminSt.MENU)
async def statistic_handler(message: types.Message):
    await bot.send_message(
        message.chat.id,
        "<b>Статистика</b>\n"
        f"<b>Количество пользователей:</b> {await User.all().count()}"
    )
