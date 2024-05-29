import asyncio
import inspect
import logging
from contextlib import suppress

import uvloop
from loguru import logger

from bot import start_bot
from config import DEBUG


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level if it exists.
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message.
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

    with suppress(KeyboardInterrupt):
        asyncio.run(start_bot(), debug=DEBUG)
