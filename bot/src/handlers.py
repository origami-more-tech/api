from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from config import Collection
from loader import dp, scheduler, firestore


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Starting jobs...")
    if not scheduler.running:
        scheduler.start()
    data = {"id": str(message.chat.id), "full_name": message.chat.full_name}
    await firestore.create(collection=Collection.Chat, data=data)
    await message.answer(f"Jobs started!")


@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    await message.answer(f"Stopping jobs...")
    scheduler.shutdown()
    await message.answer(f"Jobs stopped!")
