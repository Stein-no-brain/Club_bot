import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, request
def update_or_create_user(username):
    # Создаем подключение к базе данных SQLite
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Проверяем, существует ли пользователь в базе данных
    c.execute("SELECT * FROM users WHERE user_id=?", (username,))
    user = c.fetchone()

    if user:
        # Если пользователь существует, обновляем значение sub_time на 30
        new_sub_time = int(user[2]) + 30
        c.execute("UPDATE users SET sub_time=? WHERE user_id=?", (new_sub_time, username))
    else:
        # Если пользователь не существует, добавляем его в базу данных со значением sub_time = 30
        c.execute("INSERT INTO users (user_id, sub_time) VALUES (?, ?)", (username, 30))

    # Сохраняем изменения в базе данных и закрываем подключение
    conn.commit()
    conn.close()


def read_database():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

def decrement_sub_time():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Изменяем значение sub_time для всех пользователей
    c.execute("UPDATE users SET sub_time = sub_time - 1 WHERE sub_time > 0")

    conn.commit()
    conn.close()
    read_database()

# Обработка вебхуков от ботхелп
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    data = request.get_json()
    print(data)
    user_id = data['user_id']
    update_or_create_user(user_id)

    return 'OK'

if __name__ == '__main__':
    # Создаем планировщик
    scheduler = BackgroundScheduler()
    # Запускаем задачу каждые 5 минут
    scheduler.add_job(decrement_sub_time, 'interval', hours=24)
    scheduler.start()

    app.run()


