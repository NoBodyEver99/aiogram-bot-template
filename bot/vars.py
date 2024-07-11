from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage

from config import TELEGRAM_TOKEN, REDIS_URL

bot = Bot(
    token=TELEGRAM_TOKEN,
    default=DefaultBotProperties(
        parse_mode="HTML",
        link_preview_is_disabled=True
    ),
)
dp = Dispatcher(
    bot=bot,
    storage=RedisStorage.from_url(REDIS_URL)
)
