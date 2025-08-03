import nest_asyncio
import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.database.table import create_table

from app.handlers import router

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


async def main():
    load_dotenv()
    dp = Dispatcher()
    bot = Bot(token=os.getenv('BOT_TOKEN'))
    await create_table()
    dp.startup.register(startup)
    dp.shutdown.register(shutdown)
    dp.include_router(router)
    await dp.start_polling(bot)

async def startup(dispatcher: Dispatcher):
    print('Бот запущен')

async def shutdown(dispatcher: Dispatcher):
    print('Бот остановлен')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass