import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from config import BOT_TOKEN
from handlers import router


async def main():
    # У Aiogram 3.22 parse_mode передається як звичайний рядок
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Підключаємо роутери
    dp.include_router(router)

    # Встановлюємо команди
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the Bot"),
        BotCommand(command="films", description="Get films"),
        BotCommand(command="create_film", description="Create a film"),
    ])

    logging.info("✅ Bot is starting...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Bot stopped!")