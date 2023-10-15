import asyncio
import logging
import sys
import handlers
from loader import bot, scheduler, dp
from aiogram.types import BotCommand


async def on_startup():
    bot_commands = [
        BotCommand(command="/help", description="Информация обо мне"),
        BotCommand(command="/start", description="Запустить рекомендательную систему"),
        BotCommand(command="/stop", description="Остановить рекомендательную систему"),
    ]
    await bot.set_my_commands(bot_commands)
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
