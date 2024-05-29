from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from loguru import logger

from bot.misc.utils import extract_unique_code
from db.models import User, Referral, UtmMark


class UserMiddleware(BaseMiddleware):
    """
    Creating and returning user model
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        if isinstance(event, (CallbackQuery, Message)):
            from_user = event.from_user
        else:
            return

        user, created = await User.get_or_create(
            user_id=from_user.id,
            defaults={
                "first_name": from_user.first_name,
                "last_name": from_user.last_name,
                "username": from_user.username
            }
        )

        if created and (code := extract_unique_code(event.text)):
            if code.isdigit() and (inviter_user := await User.get_or_none(user_id=int(code))):
                await Referral.create(
                    inviter=inviter_user.id,
                    invited=user.id
                )
                logger.debug(f"New referral `{user.id}` from `{inviter_user.id}`")
            elif (utm := await UtmMark.get_or_none(name=code)):
                utm.transitions += 1
                await utm.save()
        else:
            fields_to_update = {}

            if user.first_name != from_user.first_name:
                fields_to_update["first_name"] = from_user.first_name
            if user.last_name != from_user.last_name:
                fields_to_update["last_name"] = from_user.last_name
            if user.username != from_user.username:
                fields_to_update["username"] = from_user.username

            if fields_to_update:
                await user.update_from_dict(fields_to_update)
                await user.save()

        data["user"] = user

        return await handler(event, data)
