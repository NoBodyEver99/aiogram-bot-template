from typing import Optional

from aiogram import Router, types, F
from aiogram.types import ReplyKeyboardMarkup as RKeyboard, KeyboardButton as RButton
from aiogram.fsm.context import FSMContext
from tortoise.expressions import Q

from bot.misc.utils import build_inline_keyboard
from bot.states.admin_st import AdminSt, NewsletterSt
from bot.vars import bot
from db.models import User, Newsletter, NewsletterUser

newsletter_router = Router(name="NewsletterRouter")


@newsletter_router.message(F.text == "Рассылка", AdminSt.MENU)
async def newsletter_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    keyboard = RKeyboard(resize_keyboard=True, keyboard=[
        [RButton(text="Текст"), RButton(text="Медиа")],
        [RButton(text="Клавиатура"), RButton(text="Превью")],
        [RButton(text=f"Задачи ({len(bot.newsletter.tasks)})"), RButton(text="Добавить задачу")],
        [RButton(text="Назад")]
    ])

    await bot.send_message(message.chat.id, "<b>Рассылка</b>", reply_markup=keyboard)

    if "text" not in data:
        await state.set_data({
            "text": None,
            "media": None,
            "media_type": None,
            "keyboard": None
        })
    await state.set_state(NewsletterSt.BASE)


# region Preview
@newsletter_router.message(F.text == "Превью", NewsletterSt.BASE)
async def preview_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if not any({data["text"], data["media"]}):
        await bot.send_message(message.chat.id, "<b>Укажите текст или медиа</b>")
    else:
        text = data["text"]
        media = data["media"]
        media_type = data["media_type"]
        keyboard = build_inline_keyboard(x) if (x := data["keyboard"]) else None

        if media_type == "photo":
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=media,
                caption=text,
                reply_markup=keyboard
            )
        elif media_type == "video":
            await bot.send_video(
                chat_id=message.chat.id,
                video=media,
                caption=text,
                reply_markup=keyboard
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=text,
                reply_markup=keyboard
            )
# endregion


# region Edit Text
@newsletter_router.message(F.text == "Текст", NewsletterSt.BASE)
async def edit_text_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    keyboard = [
        [RButton(text="Назад")]
    ]

    if data["text"]:
        keyboard.append([RButton(text="Удалить текст")])

    keyboard = RKeyboard(resize_keyboard=True, keyboard=keyboard)

    await bot.send_message(
        message.chat.id,
        "<b>Введите текст рассылки:</b>",
        reply_markup=keyboard
    )

    await state.set_state(NewsletterSt.TEXT)


@newsletter_router.message(F.text == "Удалить текст", NewsletterSt.TEXT)
async def delete_text_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "text": None
    })

    await bot.send_message(message.chat.id, "<b>Текст удалён</b>")

    await newsletter_handler(message, state)


@newsletter_router.message(F.text, NewsletterSt.TEXT)
async def text_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "text": message.html_text.strip()
    })

    await bot.send_message(message.chat.id, "<b>Текст изменён</b>")

    await newsletter_handler(message, state)
# endregion


# region Edit Media
@newsletter_router.message(F.text == "Медиа", NewsletterSt.BASE)
async def edit_media_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    keyboard = [
        [RButton(text="Назад")]
    ]

    if data["text"]:
        keyboard.append([RButton(text="Удалить медиа")])

    keyboard = RKeyboard(resize_keyboard=True, keyboard=keyboard)

    await bot.send_message(
        message.chat.id,
        "<b>Отправьте фото или видео для рассылки:</b>",
        reply_markup=keyboard
    )

    await state.set_state(NewsletterSt.MEDIA)


@newsletter_router.message(F.text == "Удалить медиа", NewsletterSt.MEDIA)
async def delete_media_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "media": None,
        "media_type": None
    })

    await bot.send_message(message.chat.id, "<b>Медиа удалено</b>")

    await newsletter_handler(message, state)


@newsletter_router.message(lambda m: m.photo or m.video, NewsletterSt.MEDIA)
async def media_handler(message: types.Message, state: FSMContext):
    if message.photo:
        await state.update_data({
            "media": message.photo[-1].file_id,
            "media_type": "photo"
        })
    else:
        await state.update_data({
            "media": message.video.file_id,
            "media_type": "video"
        })

    await bot.send_message(message.chat.id, "<b>Медиа изменено</b>")

    await newsletter_handler(message, state)
# endregion


# region Edit keyboard
@newsletter_router.message(F.text == "Клавиатура", NewsletterSt.BASE)
async def edit_keyboard_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    keyboard = [
        [RButton(text="Назад")]
    ]

    if data["keyboard"]:
        keyboard.append([RButton(text="Удалить Клавиатуру")])

    keyboard = RKeyboard(resize_keyboard=True, keyboard=keyboard)

    await bot.send_message(
        message.chat.id,
        "<b>Отправьте Клавиатуру в следующем формате:</b> text|url&text|url\n\n"
        "<code>|</code> - используется для разделения текста и ссылки\n"
        "<code>&</code> - используется для разделения кнопок на одном столбце\n\n"
        "<b>Новый столбец начинается с новой строки</b>",
        reply_markup=keyboard
    )

    await state.set_state(NewsletterSt.KEYBOARD)


@newsletter_router.message(F.text == "Удалить Клавиатуру", NewsletterSt.KEYBOARD)
async def delete_keyboard_handler(message: types.Message, state: FSMContext):
    await state.update_data({
        "keyboard": None
    })

    await bot.send_message(message.chat.id, "<b>Клавиатура удалена</b>")

    await newsletter_handler(message, state)


@newsletter_router.message(F.text, NewsletterSt.KEYBOARD)
async def keyboard_handler(message: types.Message, state: FSMContext):
    try:
        build_inline_keyboard((x := message.text.strip()))
    except (ValueError, IndexError):
        await bot.send_message(message.chat.id, "<b>Проверьте правильность написания и повторите попытку</b>")
    else:
        await state.update_data({
            "keyboard": x
        })

        await bot.send_message(message.chat.id, "<b>Клавиатура изменена</b>")

        await newsletter_handler(message, state)
# endregion


# region Create Task
@newsletter_router.message(F.text == "Добавить задачу", NewsletterSt.BASE)
async def create_task_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if not any({data["text"], data["media"]}):
        await bot.send_message(message.chat.id, "<b>Укажите текст или медиа</b>")
    else:
        user = await User.get(user_id=message.from_user.id)
        task = await Newsletter.create(
            owner=user,
            text=data["text"],
            media=data["media"],
            media_type=data["media_type"],
            keyboard=data["keyboard"]
        )
        bot.newsletter.tasks.append(task)

        await task_handler(message, state, task_id=task.id)
# endregion


# region Tasks
@newsletter_router.message(F.text.startswith("Задачи"), NewsletterSt.BASE)
async def tasks_handler(message: types.Message, state: FSMContext):
    keyboard = []

    for task in bot.newsletter.tasks:
        keyboard.append([RButton(text=f"Задача {task.id}")])

    keyboard.append([RButton(text="Назад")])

    await bot.send_message(
        message.chat.id,
        "<b>Список задач:</b>",
        reply_markup=RKeyboard(resize_keyboard=True, keyboard=keyboard)
    )

    await state.set_state(NewsletterSt.TASKS)


@newsletter_router.message(F.text.startswith("Задача"), NewsletterSt.TASKS)
async def task_handler(message: types.Message, state: FSMContext, task_id: Optional[int] = None):
    task_id = task_id or int(message.text.split(" ")[-1])

    if not (task := bot.newsletter.get_task_by_id(task_id)):
        await bot.send_message(message.chat.id, "<b>Задача не найдена</b>")

        await tasks_handler(message, state)

        return

    match task.status:
        case "launched":
            task_status = "Запущено"
            button_text = "Остановить"
        case "stopped":
            task_status = "Остановлено"
            button_text = "Запустить"
        case "finished":
            task_status = "Закончено"
            button_text = "Удалить"
        case _:
            task_status = "Неизвестно"
            button_text = "Удалить"

    keyboard = RKeyboard(resize_keyboard=True, keyboard=[
        [RButton(text="Превью"), RButton(text="Статистика")],
        [RButton(text="Удалить задачу"), RButton(text=button_text)],
        [RButton(text="Назад")]
    ])

    await bot.send_message(
        message.chat.id,
        f"<b>Задача №{task.id}</b>\n"
        f"<b>Статус: {task_status}</b>",
        reply_markup=keyboard
    )

    await state.update_data({
        "task_id": task_id
    })
    await state.set_state(NewsletterSt.TASK)


@newsletter_router.message(F.text == "Превью", NewsletterSt.TASK)
async def task_preview_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    task = bot.newsletter.get_task_by_id(data["task_id"])

    if task.media_type == "photo":
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=task.media,
            caption=task.text,
            reply_markup=task.keyboard
        )
    elif task.media_type == "video":
        await bot.send_video(
            chat_id=message.chat.id,
            video=task.media,
            caption=task.text,
            reply_markup=task.keyboard
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=task.text,
            reply_markup=task.keyboard
        )


@newsletter_router.message(F.text == "Статистика", NewsletterSt.TASK)
async def task_statistic_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    task = bot.newsletter.get_task_by_id(data["task_id"])

    sent_user_ids = await NewsletterUser.filter(newsletter=task).values_list("user_id", flat=True)

    remaining = await User.filter(~Q(id__in=sent_user_ids)).count()
    success = await NewsletterUser.filter(newsletter=task, success=True).count()
    failed = await NewsletterUser.filter(newsletter=task, success=False).count()

    await bot.send_message(
        chat_id=message.chat.id,
        text="<b>Статистика</b>\n"
            f"<b>Осталось:</b> {remaining}\n"
            f"<b>Отправлено:</b> {success}\n"
            f"<b>Не удалось отправить:</b> {failed}"
    )


@newsletter_router.message(F.text == "Запустить", NewsletterSt.TASK)
async def launch_task_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    task = bot.newsletter.get_task_by_id(data["task_id"])

    if task.status != "stopped":
        await task_handler(message, state, task_id=task.id)
        return

    await bot.newsletter.start_task(task)

    await bot.send_message(
        chat_id=message.chat.id,
        text="<b>Задача запущена</b>"
    )

    await task_handler(message, state, task_id=task.id)


@newsletter_router.message(F.text == "Остановить", NewsletterSt.TASK)
async def stop_task_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    task = bot.newsletter.get_task_by_id(data["task_id"])

    if task.status != "launched":
        await task_handler(message, state, task_id=task.id)
        return

    await bot.newsletter.stop_task(task)

    await bot.send_message(
        chat_id=message.chat.id,
        text="<b>Задача остановлена</b>"
    )

    await task_handler(message, state, task_id=task.id)


@newsletter_router.message(F.text.in_({"Удалить задачу", "Удалить"}), NewsletterSt.TASK)
async def delete_task_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    task = bot.newsletter.get_task_by_id(data["task_id"])

    await bot.newsletter.delete_task(task)

    await bot.send_message(
        chat_id=message.chat.id,
        text="<b>Задача удалена</b>"
    )

    await tasks_handler(message, state)
# endregion
