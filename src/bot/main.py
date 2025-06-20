import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from bot.middlewares import AddUserMiddleware, AccessMiddleware
from bot.handlers import start, admin

load_dotenv()


async def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN не найден в .env")

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    dp.message.middleware(AddUserMiddleware())
    dp.message.middleware(AccessMiddleware())

    dp.include_routers(start.router, admin.router)

    print("[DEBUG] Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
