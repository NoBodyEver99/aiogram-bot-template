import aiohttp
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loguru import logger


def extract_unique_code(text: str):
    return words[1] if len((words := text.split())) > 1 else None


def build_inline_keyboard(text: str) -> InlineKeyboardMarkup:
    keyboard = []

    for column in text.strip().split("\n"):
        keyboard.append(
            [
                InlineKeyboardButton(text=text.strip(), url=url.strip())

                for text, url in [
                    _.split("|")
                    for _ in column.split("&")]
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
