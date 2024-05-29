import asyncio
from typing import List, Dict

import aiojobs
from aiogram.exceptions import AiogramError
from aiojobs import Job
from loguru import logger
from tortoise.expressions import Q

from bot.misc.utils import build_inline_keyboard
from bot.vars import bot
from db.models import User, Newsletter, NewsletterUser


class NewsletterManager:
    def __init__(self, jobs_limit: int = 10):
        self.scheduler = aiojobs.Scheduler(
            close_timeout=0.1,
            limit=jobs_limit,
            pending_limit=1000
        )
        self.tasks: List[Newsletter] = []
        self.jobs: Dict[int, Job] = {}
        self.latency = lambda: 1 / (30 / self.scheduler.active_count) * 1.2  # 1 / (max requests per second / active tasks) * safety airbag

    async def init(self):
        self.tasks = await Newsletter.all()

        for newsletter in self.tasks:
            if newsletter.status == "launched":
                await self.start_task(newsletter)

    async def start_task(self, newsletter: Newsletter):
        newsletter.status = "launched"
        await newsletter.save()

        job = await self.scheduler.spawn(self.task_core(newsletter), str(newsletter.id))

        self.jobs[newsletter.id] = job

    async def stop_task(self, newsletter: Newsletter):
        newsletter.status = "stopped"
        await newsletter.save()

        await self.jobs[newsletter.id].close()

    async def delete_task(self, newsletter: Newsletter):
        self.tasks.remove(newsletter)
        self.jobs.pop(newsletter.id, None)
        await newsletter.delete()

    def get_task_by_id(self, task_id: int) -> Newsletter | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    async def task_core(self, newsletter: Newsletter):
        keyboard = build_inline_keyboard(newsletter.keyboard) if newsletter.keyboard else None

        if newsletter.media:
            if newsletter.media_type == "photo":
                task_func = lambda chat_id: bot.send_photo(chat_id, photo=newsletter.media, caption=newsletter.text, reply_markup=keyboard)
            else:
                task_func = lambda chat_id: bot.send_video(chat_id, video=newsletter.media, caption=newsletter.text, reply_markup=keyboard)
        else:
            task_func = lambda chat_id: bot.send_message(chat_id, text=newsletter.text, reply_markup=keyboard)

        sent_user_ids = await NewsletterUser.filter(newsletter=newsletter).values_list("user_id", flat=True)

        users = await User.filter(~Q(id__in=sent_user_ids))

        for user in users:
            try:
                await task_func(user.user_id)
            except AiogramError as e:
                await NewsletterUser.create(newsletter=newsletter, user=user, success=False)

                logger.debug(f"Failed sent newsletter to \"{user.user_id}\": {e}")
            else:
                await NewsletterUser.create(newsletter=newsletter, user=user, success=True)
            finally:
                await asyncio.sleep(self.latency())

        owner = await newsletter.owner.get()

        await bot.send_message(
            chat_id=owner.user_id,
            text=f"Ваша задача №{newsletter.id} завершена!"
        )

        newsletter.status = "finished"
        await newsletter.save()
