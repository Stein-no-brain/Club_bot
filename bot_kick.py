from aiogram import Dispatcher, Bot, types
# from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import sqlite3
import logging
import asyncio

from config2 import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

chat_id = -1001793387741
bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
dp = Dispatcher()
scheduler = AsyncIOScheduler

async def check_users_for_kick():
    # chat = await bot.get_chat(chat_id)
    # members = await bot.get_chat_member(chat_id)

    # Создаем подключение к базе данных SQLite
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Получаем список пользователей, у которых sub_time = 0
    c.execute("SELECT user_id FROM users WHERE sub_time = 0")
    users = c.fetchall()

    # Если есть пользователи с sub_time = 0, то выгоняем их из чата
    for user in users:
        user_id = user[0]
        try:
            await bot.ban_chat_member(chat_id=chat_id, user_id=int(user_id))
            await bot.unban_chat_member(chat_id=chat_id, user_id=int(user_id))
            c.execute("DELETE FROM users WHERE user_id=?", (user_id,))
        except Exception as ex:
            logging.error(f'[Exception] - {ex}', exc_info=True)
async def main():
    # Создаем планировщик
    scheduler = AsyncIOScheduler()
    # Запускаем задачу каждые 24 часа
    scheduler.add_job(check_users_for_kick, 'interval', hours=1)
    scheduler.start()
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    asyncio.run(main())