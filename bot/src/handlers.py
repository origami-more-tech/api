from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import Collection
from loader import dp, scheduler, firestore
from utils import is_job_running, ping


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    chat_id = str(message.chat.id)
    data = {"id": chat_id, "full_name": message.chat.full_name}
    if not is_job_running(chat_id):
        await message.answer(f"Starting job...")
        scheduler.add_job(ping, "interval", seconds=10, id=chat_id, args=(chat_id,))
        await firestore.create(collection=Collection.Chat, data=data)
        await message.answer(f"Job started!")
    else:
        await message.answer(f"Job already runs!")


@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    chat_id = str(message.chat.id)
    if is_job_running(chat_id):
        await message.answer(f"Stopping job...")
        scheduler.pause_job(chat_id)
        scheduler.remove_job(chat_id)
        await message.answer(f"Job stopped!")
    else:
        await message.answer(f"Job already stopped!")
