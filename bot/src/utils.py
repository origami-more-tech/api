from loader import scheduler, bot


def is_job_running(job_id: str) -> bool:
    return job_id in [job.id for job in scheduler.get_jobs()]


async def ping(chat_id: str):
    await bot.send_message(chat_id=chat_id, text="ping")
