import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from PIL import Image, ImageTk

class TaskMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster")

        # Подключение к базе данных
        self.conn = sqlite3.connect('taskmaster.db')
        self.create_tables()

        # Остальные инициализации интерфейса
        self.login_page()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                task TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        # Добавьте другие таблицы по необходимости (например, для друзей и т.д.)
        self.conn.commit()

    def login_page(self):
        self.clear_frame()
        self.root.geometry("210x150")
        self.root.title("Login")

        label_username = tk.Label(self.root, text="Username:")
        label_password = tk.Label(self.root, text="Password:")
        entry_username = tk.Entry(self.root)
        entry_password = tk.Entry(self.root, show="*")
        btn_login = tk.Button(self.root, text="Login", command=lambda: self.login(entry_username.get(), entry_password.get()))
        btn_register = tk.Button(self.root, text="Register", command=self.register_page)

        label_username.grid(row=0, column=0, padx=5, pady=5)
        entry_username.grid(row=0, column=1, padx=5, pady=5)
        label_password.grid(row=1, column=0, padx=5, pady=5)
        entry_password.grid(row=1, column=1, padx=5, pady=5)
        btn_login.grid(row=2, column=0, columnspan=2, pady=10)
        btn_register.grid(row=3, column=0, columnspan=2)

    def register_page(self):
        self.clear_frame()
        self.root.geometry("210x150")
        self.root.title("Register")

        label_username = tk.Label(self.root, text="Username:")
        label_password = tk.Label(self.root, text="Password:")
        entry_username = tk.Entry(self.root)
        entry_password = tk.Entry(self.root, show="*")
        btn_register = tk.Button(self.root, text="Register", command=lambda: self.register(entry_username.get(), entry_password.get()))
        btn_back = tk.Button(self.root, text="Back", command=self.login_page)

        label_username.grid(row=0, column=0, padx=5, pady=5)
        entry_username.grid(row=0, column=1, padx=5, pady=5)
        label_password.grid(row=1, column=0, padx=5, pady=5)
        entry_password.grid(row=1, column=1, padx=5, pady=5)
        btn_register.grid(row=2, column=0, columnspan=2, pady=10)
        btn_back.grid(row=3, column=0, columnspan=2)

    def menu_page(self):
        self.clear_frame()
        self.root.geometry("250x200")
        self.root.title("Menu")

        btn_tasks = tk.Button(self.root, text="Tasks", command=self.tasks_page)
        btn_friends = tk.Button(self.root, text="Friends", command=self.friends_page)
        btn_settings = tk.Button(self.root, text="Settings", command=self.settings_page)
        btn_logout = tk.Button(self.root, text="Logout", command=self.login_page)

        btn_tasks.pack(pady=10)
        btn_friends.pack(pady=10)
        btn_settings.pack(pady=10)
        btn_logout.pack(pady=10)

    # def tasks_page(self):
    #     self.clear_frame()
    #     self.root.geometry("500x300")
    #     self.root.title("Tasks")

    #     # Получаем список задач для текущего пользователя из базы данных
    #     tasks = self.get_user_tasks()

    #     # Создаем список задач
    #     task_listbox = tk.Listbox(self.root, width=40, height=10)
    #     for task in tasks:
    #         task_listbox.insert(tk.END, task)

    #     # Добавляем элементы управления
    #     btn_add_task = tk.Button(self.root, text="Add Task", command=self.add_task)
    #     btn_edit_task = tk.Button(self.root, text="Edit Task", command=lambda: self.edit_task(task_listbox))
    #     btn_delete_task = tk.Button(self.root, text="Delete Task", command=lambda: self.delete_task(task_listbox))
    #     btn_back = tk.Button(self.root, text="Back", command=self.menu_page)

    #     # Отображаем элементы
    #     task_listbox.pack(pady=10)
    #     btn_add_task.pack(pady=5)
    #     btn_edit_task.pack(pady=5)
    #     btn_delete_task.pack(pady=5)
    #     btn_back.pack(pady=10)

    def friends_page(self):
        self.clear_frame()
        self.root.geometry("500x300")
        self.root.title("Friends")

        # Реализуйте логику страницы друзей

        btn_back = tk.Button(self.root, text="Back", command=self.menu_page)
        btn_back.pack(pady=10)

    def settings_page(self):
        self.clear_frame()
        self.root.geometry("300x150")
        self.root.title("Settings")

        # Реализуйте логику страницы настроек

        btn_back = tk.Button(self.root, text="Back", command=self.menu_page)
        btn_back.pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()

        if user:
            self.menu_page()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def register(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        self.conn.commit()
        messagebox.showinfo("Registration Successful", "You are now registered")
        self.login_page()

    def get_user_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT task FROM tasks WHERE user_id=?", (1,))  # Здесь используйте ID текущего пользователя
        tasks = cursor.fetchall()
        return [task[0] for task in tasks]

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter task:")
        if task:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO tasks (user_id, task) VALUES (?, ?)", (1, task))  # Здесь используйте ID текущего пользователя
            self.conn.commit()
            self.tasks_page()

    def edit_task(self, task_listbox):
        selected_task_index = task_listbox.curselection()
        if selected_task_index:
            current_task = task_listbox.get(selected_task_index)
            new_task = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=current_task)
            if new_task:
                cursor = self.conn.cursor()
                cursor.execute("UPDATE tasks SET task=? WHERE task=?", (new_task, current_task))
                self.conn.commit()
                self.tasks_page()

    def delete_task(self, task_listbox):
        selected_task_index = task_listbox.curselection()
        if selected_task_index:
            current_task = task_listbox.get(selected_task_index)
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE task=?", (current_task,))
            self.conn.commit()
            self.tasks_page()
    def tasks_page(self):
        self.clear_frame()
        self.root.geometry("500x400")
        self.root.title("Tasks")

        # Получаем список задач для текущего пользователя из базы данных
        tasks = self.get_user_tasks()

        # Создаем список задач
        task_listbox = tk.Listbox(self.root, width=40, height=10)
        for task in tasks:
            task_listbox.insert(tk.END, task)

        # Добавляем элементы управления
        btn_add_task = tk.Button(self.root, text="Add Task", command=self.add_task)
        btn_edit_task = tk.Button(self.root, text="Edit Task", command=lambda: self.edit_task(task_listbox))
        btn_delete_task = tk.Button(self.root, text="Delete Task", command=lambda: self.delete_task(task_listbox))
        btn_back = tk.Button(self.root, text="Back", command=self.tasks_page_back)  # Новая кнопка "Назад"

        # Отображаем элементы
        task_listbox.pack(pady=10)
        btn_add_task.pack(pady=5)
        btn_edit_task.pack(pady=5)
        btn_delete_task.pack(pady=5)
        btn_back.pack(pady=10)

    def tasks_page_back(self):
        self.menu_page()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskMasterApp(root)
    root.mainloop()
