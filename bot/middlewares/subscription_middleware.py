from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup as IKeyboard, InlineKeyboardButton as IButton
from loguru import logger

from bot.misc.utils import extract_unique_code
from bot.vars import bot
from db.models import Channel


class SubscriptionMiddleware(BaseMiddleware):
    """
    Creating and returning user model
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user = data["user"]
        channels_keyboard = []

        for channel in await Channel.all():
            user = await bot.get_chat_member(channel.id, user.user_id)

            if not user.is_member:
                channels_keyboard.append([IButton(text=channel.title, url=channel.url)])

        if channels_keyboard:
            channels_keyboard.append([IButton(text="✅ Я подписался", callback_data="CheckSubscription")])

            await bot.send_message(
                event.from_user.id,
                "Чтобы пользоваться ботом вы должны подписаться на каналы",
                reply_markup=IKeyboard(inline_keyboard=channels_keyboard)
            )
        else:
            return await handler(event, data)
