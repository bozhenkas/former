import asyncio
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message

from bot.middlewares.add_user import AddUserMiddleware
from bot.handlers import start

load_dotenv()  # Загружаем переменные из .env


async def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token:
        raise ValueError("TELEGRAM_TOKEN не найден в .env")

    bot = Bot(token=token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    # Регистрируем middleware для сообщений и колбеков
    dp.message.middleware(AddUserMiddleware())
    dp.callback_query.middleware(AddUserMiddleware())

    dp.include_routers(start.router)

    print("[DEBUG] Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
