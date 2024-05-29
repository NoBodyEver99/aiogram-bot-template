from aiogram import Router, types, F
from aiogram.exceptions import AiogramError
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup as RKeyboard, KeyboardButton as RButton, KeyboardButtonRequestChat

from bot.states.admin_st import AdminSt, ChannelSt
from bot.vars import bot
from db.models import Channel

channel_router = Router(name="ChannelRouter")


@channel_router.message(F.text == "Каналы", AdminSt.MENU)
async def channels_handler(message: types.Message, state: FSMContext):
    channels = await Channel.all()
    keyboard = []

    for channel in channels:
        keyboard.append([RButton(text=f"Канал {channel.title}")])

    keyboard.extend([
        [RButton(text="Добавить канал", request_chat=KeyboardButtonRequestChat(
            request_id=777,
            chat_is_channel=True,
            bot_is_member=True,
            bot_administrator_rights=None
        ))],
        [RButton(text="Назад")]
    ])

    await bot.send_message(
        message.chat.id,
        "<b>Список каналов</b>",
        reply_markup=RKeyboard(keyboard=keyboard, resize_keyboard=True)
    )
    await state.set_state(ChannelSt.BASE)


@channel_router.message(F.chat_shared, ChannelSt.BASE)
async def chat_shared_handler(message: types.Message, state: FSMContext):
    try:
        chat = await bot.get_chat(message.chat_shared.chat_id)
    except AiogramError:
        await bot.send_message(message.chat.id, "<b>Добавьте бота в канал с правами администратора</b>")
    else:
        invite = await chat.create_invite_link(f"{bot.info.username} OP")

        await Channel.create(
            chat_id=chat.id,
            title=chat.title,
            url=invite.invite_link
        )

        await bot.send_message(message.chat.id, "<b>Канал добавлен</b>")
        await channels_handler(message, state)


@channel_router.message(F.text.startswith("Канал"), ChannelSt.BASE)
async def channel_handler(message: types.Message, state: FSMContext):
    channel_name = message.text.split(" ", 1)[-1]

    if (channel := await Channel.get_or_none(title=channel_name)):
        keyboard = [
            [RButton(text="Удалить канал")],
            [RButton(text="Назад")]
        ]

        await bot.send_message(
            chat_id=message.chat.id,
            text=f"<b>Канал \"{channel.title}\"</b>\n"
                 f"<b>Ссылка:</b> {channel.url}",
            reply_markup=RKeyboard(keyboard=keyboard, resize_keyboard=True)
        )
        await state.set_data({
            "channel": channel.__dict__
        })
        await state.set_state(ChannelSt.CHANNEL)
    else:
        await bot.send_message(message.chat.id, "Канал не найден")
        await channels_handler(message, state)


@channel_router.message(F.text == "Удалить канал", ChannelSt.CHANNEL)
async def delete_channel_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    channel = await Channel.get_or_none(id=data["channel"]["id"])

    if channel:
        await channel.delete()

        await bot.send_message(message.chat.id, "<b>Канал удалён</b>")
    await channels_handler(message, state)
