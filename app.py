from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'ugolnikov'

# Создаем подключение к базе данных SQLite
conn = sqlite3.connect('tasks.db', check_same_thread=False)
cursor = conn.cursor()

# Создаем таблицу пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

# Добавляем столбец "completed" в таблицу задач
try:
    cursor.execute('ALTER TABLE tasks ADD COLUMN completed INTEGER DEFAULT 0;')
    conn.commit()
except sqlite3.OperationalError:
    # Исключение вызывается, если столбец уже существует
    pass

# Создаем таблицу задач
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        task TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
''')
conn.commit()

@app.route('/complete_task/<int:task_id>', methods=['POST'])
def complete_task(task_id):
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute('UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?', (task_id, user_id))
        conn.commit()
        return '', 204  # Возвращаем пустой ответ со статусом 204 (No Content)

    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute('SELECT task, id, completed FROM tasks WHERE user_id = ?', (user_id,))
        tasks = cursor.fetchall()
        return render_template('index.html', tasks=tasks)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
        conn.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            session['user_id'] = user[0]  # Устанавливаем сессионную переменную user_id
            return redirect(url_for('index'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add_task', methods=['POST'])
def add_task():
    if 'user_id' in session:
        user_id = session['user_id']
        task = request.form['task']

        cursor.execute('INSERT INTO tasks (user_id, task) VALUES (?, ?)', (user_id, task))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    if 'user_id' in session:
        user_id = session['user_id']
        edited_task = request.form['edited_task']

        cursor.execute('UPDATE tasks SET task = ? WHERE id = ? AND user_id = ?', (edited_task, task_id, user_id))
        conn.commit()

        return '', 204  # Возвращаем пустой ответ со статусом 204 (No Content)

    return redirect(url_for('login'))

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    if 'user_id' in session:
        user_id = session['user_id']
        cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        conn.commit()
        return '', 204  # Возвращаем пустой ответ со статусом 204 (No Content)

    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
