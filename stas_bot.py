import contextlib
from aiogram import Dispatcher, Bot, types, F
from aiogram.types import ChatJoinRequest
import sqlite3
import logging
import asyncio

from config1 import Config, load_config

config: Config = load_config()
BOT_TOKEN: str = config.tg_bot.token

CHANNEL_ID = -1001793387741
def in_database(user_id):
    # Создаем подключение к базе данных SQLite
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Проверяем, существует ли пользователь в базе данных
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = c.fetchone()

    # Проверяем, что пользователь найден и sub_time больше 0
    if user and user[2] > 0:
        # Сохраняем изменения в базе данных и закрываем подключение
        conn.commit()
        conn.close()
        return True
    else:
        # Если пользователя нет или sub_time <= 0, закрываем подключение и возвращаем False
        conn.close()
        return False

async def approve_request(chat_join: ChatJoinRequest, bot: Bot):
    if in_database(chat_join.from_user.id) == True:
        await chat_join.approve()
    else:
        await chat_join.decline()

async def start():
    logging.basicConfig(level=logging.DEBUG)
    bot: Bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.chat_join_request.register(approve_request, F.chat.id == CHANNEL_ID)

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f'[Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())





