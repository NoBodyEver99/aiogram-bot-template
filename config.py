from decouple import config

TELEGRAM_TOKEN = config("BOT_TOKEN", cast=str)

ADMINS = [int(admin_id) for admin_id in config("ADMINS", cast=str).split(',')]

DATABASE_URL = config("DATABASE_URL", cast=str)
REDIS_URL = config("REDIS_URL", cast=str)

DEBUG = config("DEBUG", default=False, cast=bool)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
