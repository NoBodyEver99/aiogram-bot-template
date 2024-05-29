from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from bot.middlewares import UserMiddleware
from bot.routers.admin.admin import admin_handler
from bot.routers.admin.channel import channels_handler
from bot.routers.admin.newsletter import newsletter_handler, tasks_handler
from bot.routers.admin.utm import utms_handler
from bot.states.admin_st import NewsletterSt, ChannelSt, UtmSt

back_router = Router(name="BackRouter")
# Middlewares
back_router.message.middleware.register(UserMiddleware())


@back_router.message(F.text == "Назад")
async def back_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    match current_state:
        # region Admin States
        # To Menu
        case NewsletterSt.BASE.state | ChannelSt.BASE.state | UtmSt.BASE.state:
            await admin_handler(message, state)
        # Newsletter
        case NewsletterSt.TEXT.state | NewsletterSt.MEDIA.state | NewsletterSt.KEYBOARD.state | NewsletterSt.TASKS.state:
            await newsletter_handler(message, state)
        case NewsletterSt.TASK.state:
            await tasks_handler(message, state)
        case ChannelSt.CHANNEL.state:
            await channels_handler(message, state)
        case UtmSt.UTM.state | UtmSt.ADD_UTM.state:
            await utms_handler(message, state)
        # endregion
        case _:
            logger.warning(f"Missing handler for going back from the \"{current_state}\" state")
