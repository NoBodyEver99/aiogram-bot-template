from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.middlewares import UserMiddleware, SubscriptionMiddleware
from bot.states.user_st import UserSt
from bot.vars import bot

user_router = Router(name="UserRouter")
# Middlewares
user_router.message.middleware.register(UserMiddleware())
user_router.callback_query.middleware.register(UserMiddleware())
user_router.message.middleware.register(SubscriptionMiddleware())
user_router.callback_query.middleware.register(SubscriptionMiddleware())


@user_router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await bot.send_message(
        chat_id=message.chat.id,
        text="Меню"
    )

    await state.set_state(UserSt.MENU)


@user_router.callback_query(F.data == "CheckSubscription")
async def check_subscription_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(
        "Вы успешно подписались",
        reply_markup=None
    )
    await start_handler(call.message, state)
