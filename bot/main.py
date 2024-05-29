import aiojobs
from loguru import logger

from newsletter import NewsletterManager
from bot.routers import other_router, user_router, admin_router
from bot.vars import dp, bot
from db import init_database


@dp.startup()
async def on_startup():
    bot.info = await bot.get_me()
    bot.scheduler = aiojobs.Scheduler(
        close_timeout=0.1,
        limit=100,
        pending_limit=10000
    )
    bot.newsletter = NewsletterManager()
    await bot.newsletter.init()
    logger.success(f"Bot @{bot.info.username} launched!")


@dp.shutdown()
async def on_shutdown():
    if hasattr(bot, "scheduler") and bot.scheduler:
        await bot.scheduler.close()
    logger.success(f"Bot @{bot.info.username} shutdown!")


async def start_bot():
    """Starts the bot"""
    await init_database()

    # Including Routers
    dp.include_routers(
        other_router,
        user_router,
        admin_router
    )

    # Starting Bot
    await dp.start_polling(bot)
