from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup as RKeyboard, KeyboardButton as RButton

from bot.states.admin_st import AdminSt, UtmSt
from bot.vars import bot
from db.models import UtmMark

utm_router = Router(name="UtmRouter")


@utm_router.message(F.text == "UTM-Метки", AdminSt.MENU)
async def utms_handler(message: types.Message, state: FSMContext):
    utm_marks = await UtmMark.all()

    keyboard = []

    for utm_mark in utm_marks:
        keyboard.append([RButton(text=f"UTM {utm_mark.name}")])

    keyboard.extend([
        [RButton(text="Добавить UTM-Метку")],
        [RButton(text="Назад")]
    ])

    await bot.send_message(
        message.chat.id,
        "<b>Список UTM-Меток</b>",
        reply_markup=RKeyboard(keyboard=keyboard, resize_keyboard=True)
    )
    await state.set_state(UtmSt.BASE)


@utm_router.message(F.text.startswith("UTM"), UtmSt.BASE)
async def utm_handler(message: types.Message, state: FSMContext):
    utm_name = message.text.split(" ", 1)[-1]

    if (utm_mark := await UtmMark.get_or_none(name=utm_name)):
        keyboard = [
            [RButton(text="Удалить UTM-Метку")],
            [RButton(text="Назад")]
        ]

        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b>UTM-Метка \"{utm_mark.name}\"</b>\n"
                 f"<b>Количество переходов:</b> {utm_mark.transitions}\n"
                 f"<b>Ссылка:</b> https://t.me/{bot.info.username}?start={utm_mark.name}",
            reply_markup=RKeyboard(keyboard=keyboard, resize_keyboard=True)
        )
        await state.set_data({
            "utm": utm_mark.__dict__
        })
        await state.set_state(UtmSt.UTM)
    else:
        await bot.send_message(message.chat.id, "Метка не найдена")
        await utms_handler(message, state)


@utm_router.message(F.text == "Удалить UTM-Метку", UtmSt.UTM)
async def delete_utm_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    utm_mark = await UtmMark.get_or_none(id=data["utm"]["id"])

    if utm_mark:
        await utm_mark.delete()

        await bot.send_message(message.chat.id, "<b>UTM-Метка удалена</b>")
    await utms_handler(message, state)


@utm_router.message(F.text == "Добавить UTM-Метку", UtmSt.BASE)
async def add_utm_handler(message: types.Message, state: FSMContext):
    await bot.send_message(
        message.chat.id,
        "<b>Отправьте название для новой UTM-Метки (без пробелов)</b>",
        reply_markup=RKeyboard(keyboard=[[RButton(text="Назад")]], resize_keyboard=True)
    )
    await state.set_state(UtmSt.ADD_UTM)


@utm_router.message(F.text, UtmSt.ADD_UTM)
async def new_utm_name_handler(message: types.Message, state: FSMContext):
    utm_mark, created = await UtmMark.get_or_create(name=message.text.strip().replace(" ", ""))

    if created:
        await bot.send_message(message.chat.id, f"<b>UTM-Метка \"{utm_mark.name}\" создана</b>")
        await utms_handler(message, state)
    else:
        await bot.send_message(message.chat.id, "<b>UTM-Метка с таким именем уже существует</b>")
