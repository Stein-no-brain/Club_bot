import sqlite3

 # Создаем подключение к базе данных SQLite
conn = sqlite3.connect('database.db')
c = conn.cursor()
# Проверяем, существует ли таблица users
c.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='users' ''')
if c.fetchone()[0]==1:
    print('Таблица users уже существует.')
else:
   # Создаем таблицу users
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
            sub_time INTEGER
        );
    ''')
    print('Таблица users создана успешно.')

# Закрываем подключение к базе данных
conn.close()


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

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('database.db')
c = conn.cursor()

# Удаляем все записи из таблицы users
c.execute("DELETE FROM users")

# Сохраняем изменения в базе данных и закрываем подключение
conn.commit()
conn.close()


