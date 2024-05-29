from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "channels" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "chat_id" BIGINT NOT NULL UNIQUE,
    "title" VARCHAR(64) NOT NULL,
    "url" VARCHAR(64) NOT NULL,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "user_id" BIGINT NOT NULL UNIQUE,
    "first_name" VARCHAR(128) NOT NULL,
    "last_name" VARCHAR(128),
    "username" VARCHAR(64),
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS "newsletter" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "status" VARCHAR(8) NOT NULL  DEFAULT 'stopped',
    "text" TEXT,
    "media" VARCHAR(128),
    "media_type" VARCHAR(8),
    "keyboard" TEXT,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "owner_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "newsletter_users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "success" BOOL NOT NULL  DEFAULT False,
    "newsletter_id" INT NOT NULL REFERENCES "newsletter" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_newsletter__newslet_136a77" UNIQUE ("newsletter_id", "user_id")
);
CREATE TABLE IF NOT EXISTS "referrals" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" TIMESTAMPTZ   DEFAULT CURRENT_TIMESTAMP,
    "invited_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE,
    "inviter_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "utm_marks" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "name" VARCHAR(64) NOT NULL UNIQUE,
    "transitions" INT NOT NULL  DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "models.NewsletterUser" (
    "newsletter_id" INT NOT NULL REFERENCES "newsletter" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "users" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
