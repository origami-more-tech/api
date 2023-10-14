import asyncio
import logging
import sys
import handlers
from loader import bot, scheduler, dp


async def on_startup():
    scheduler.start()


async def on_shutdown():
    scheduler.shutdown()


async def main():
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
