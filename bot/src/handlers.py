from datetime import datetime
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types


from config import Collection
from loader import dp, scheduler, firestore
from utils import is_job_running, ping


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="Карта", callback_data="карта"))
    builder.add(types.InlineKeyboardButton(text="Кредит", callback_data="кредит"))
    builder.add(types.InlineKeyboardButton(text="Бизнес", callback_data="бизнес"))
    builder.add(types.InlineKeyboardButton(text="Пенсия", callback_data="пенсия"))
    builder.adjust(2, 2)
    await message.answer(
        "Выберите интересующую Вас категорию", reply_markup=builder.as_markup()
    )


@dp.callback_query()
async def send_random_value(callback: types.CallbackQuery):
    message: Message = callback.message  # type: ignore
    chat_id = str(message.chat.id)
    data = {"id": chat_id, "full_name": message.chat.full_name}
    if not is_job_running(chat_id):
        await message.answer(f"Настраиваем рекомендательную систему...")
        scheduler.add_job(
            ping, "interval", seconds=15, id=chat_id, args=(chat_id, callback.data)
        )
        await firestore.create(collection=Collection.Chat, data=data)
        await message.answer(
            f"Настройка прошла успешно! Интересные статьи будут приходить каждые 15 секунд. Чтобы остановить поток новостей, воспользуйтесь командой /stop"
        )
        await ping(chat_id, str(callback.data))
    else:
        await message.answer(f"Рекомендательная система уже настроена.")


@dp.message(Command("stop"))
async def command_stop_handler(message: Message) -> None:
    chat_id = str(message.chat.id)
    if is_job_running(chat_id):
        await message.answer(f"Остановка рекомендательной системы...")
        scheduler.pause_job(chat_id)
        scheduler.remove_job(chat_id)
        await message.answer(f"Остановка прошла успешно.")
    else:
        await message.answer(f"Рекомендательная система не запущена.")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        f"Привет! Я бот ВТБ, прибыл в этот мир, чтобы каждый день рекомендовать Вам интересные статьи, полные версии которых можно прочитать на сайте ВТБ."
    )
