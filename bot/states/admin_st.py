from aiogram.fsm.state import StatesGroup, State


class AdminSt(StatesGroup):
    MENU = State()


class NewsletterSt(StatesGroup):
    BASE = State()
    TEXT = State()
    MEDIA = State()
    KEYBOARD = State()
    TASKS = State()
    TASK = State()


class ChannelSt(StatesGroup):
    BASE = State()
    CHANNEL = State()


class UtmSt(StatesGroup):
    BASE = State()
    UTM = State()
    ADD_UTM = State()
