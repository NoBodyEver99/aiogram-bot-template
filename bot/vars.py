from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from config import TELEGRAM_TOKEN, REDIS_URL

bot = Bot(
    token=TELEGRAM_TOKEN,
    parse_mode="HTML",
    disable_web_page_preview=True
)
dp = Dispatcher(
    bot=bot,
    storage=RedisStorage.from_url(REDIS_URL)
)
