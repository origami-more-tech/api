import asyncio
import logging
import sys
import handlers
from loader import bot, scheduler, dp, firestore
from config import Collection


async def ping():
    chats = await firestore.get_all(collection=Collection.Chat)
    for chat in chats:
        await bot.send_message(chat_id=chat["id"], text="ping")


def on_startup():
    scheduler.add_job(ping, "interval", seconds=10)


def on_shutdown():
    scheduler.shutdown()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
