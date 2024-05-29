from typing import NoReturn

import asyncpg
from loguru import logger
from tortoise import Tortoise
from tortoise.exceptions import DBConnectionError

from config import DATABASE_URL, TORTOISE_ORM


async def init_database() -> NoReturn:
    """
    Initializes the database
    """
    logger.debug("Database initialization")

    while True:
        try:
            await Tortoise.init(config=TORTOISE_ORM)
            await Tortoise.generate_schemas()
        except DBConnectionError:
            split_url = DATABASE_URL.split("/")
            db_name = split_url[-1]
            conn = await asyncpg.connect("/".join(split_url[:-1]))

            try:
                await conn.execute(f'CREATE DATABASE {db_name}')
            except Exception as e:
                print(f"Failed to create `{db_name}` database: {e}")
            else:
                logger.success(f"The `{db_name}` database has been created")
            finally:
                await conn.close()
        else:
            logger.success("Database initialized")
            break
