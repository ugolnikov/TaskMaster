import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog  
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
            password TEXT,
            profile_picture BLOB
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
        self.root.geometry("300x200")
        self.root.title("Register")

        label_username = tk.Label(self.root, text="Username:")
        label_password = tk.Label(self.root, text="Password:")
        label_profile_picture = tk.Label(self.root, text="Profile Picture:")
        entry_username = tk.Entry(self.root)
        entry_password = tk.Entry(self.root, show="*")
        btn_register = tk.Button(self.root, text="Register", command=lambda: self.register(entry_username.get(), entry_password.get()))
        btn_back = tk.Button(self.root, text="Back", command=self.login_page)
        btn_upload_picture = tk.Button(self.root, text="Upload Picture", command=self.upload_profile_picture)

        self.profile_picture_label = tk.Label(self.root, text="No Picture")
        self.profile_picture_label.grid(row=0, column=2, rowspan=4, padx=10)

        label_username.grid(row=0, column=0, padx=5, pady=5)
        entry_username.grid(row=0, column=1, padx=5, pady=5)
        label_password.grid(row=1, column=0, padx=5, pady=5)
        entry_password.grid(row=1, column=1, padx=5, pady=5)
        label_profile_picture.grid(row=2, column=0, padx=5, pady=5)
        btn_upload_picture.grid(row=2, column=1, padx=5, pady=5)
        btn_register.grid(row=3, column=0, columnspan=2, pady=10)
        btn_back.grid(row=4, column=0, columnspan=2)
    def upload_profile_picture(self):
        file_path = filedialog.askopenfilename(title="Select Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if file_path:
            image = Image.open(file_path)
            image.thumbnail((50, 50))
            photo = ImageTk.PhotoImage(image)
            self.profile_picture_label.config(image=photo, text="")
            self.profile_picture_label.image = photo
            self.profile_picture_label.file_path = file_path
        print(image, file_path)


    def menu_page(self, user):
        self.clear_frame()
        self.root.geometry("250x200")
        self.root.title("Menu")

    # Extract user ID
        user_id = user[0]

    # Получаем фото профиля пользователя из базы данных
        profile_picture_data = self.get_profile_picture(user_id)

    # Отображаем фото профиля в самом верху по центру
        if profile_picture_data:
            profile_image = ImageTk.PhotoImage(data=profile_picture_data)
            profile_label = tk.Label(self.root, image=profile_image)
            profile_label.image = profile_image
            profile_label.pack(pady=10)

        btn_tasks = tk.Button(self.root, text="Tasks", command=lambda: self.tasks_page(user_id))
        btn_friends = tk.Button(self.root, text="Friends", command=self.friends_page)
        btn_settings = tk.Button(self.root, text="Settings", command=self.settings_page)
        btn_logout = tk.Button(self.root, text="Logout", command=self.login_page)

        btn_tasks.pack(pady=10)
        btn_friends.pack(pady=10)
        btn_settings.pack(pady=10)
        btn_logout.pack(pady=10)


    def tasks_page(self):
        self.clear_frame()
        self.root.geometry("500x400")
        self.root.title("Tasks")

        # Получаем фото профиля пользователя из базы данных
        profile_picture_data = self.get_profile_picture()

        # Отображаем фото профиля справа
        if profile_picture_data:
            profile_image = ImageTk.PhotoImage(data=profile_picture_data)
            profile_label = tk.Label(self.root, image=profile_image)
            profile_label.image = profile_image
            profile_label.grid(row=0, column=1, rowspan=4, padx=10)

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
        task_listbox.grid(row=0, column=0, pady=10)
        btn_add_task.grid(row=1, column=0, pady=5)
        btn_edit_task.grid(row=2, column=0, pady=5)
        btn_delete_task.grid(row=3, column=0, pady=5)
        btn_back.grid(row=4, column=0, pady=10)

    # Добавим метод для получения фото профиля пользователя из базы данных
    def get_profile_picture(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT profile_picture FROM users WHERE id=?", (user_id,))
        profile_picture_data = cursor.fetchone()
        return profile_picture_data[0] if (profile_picture_data and profile_picture_data[0]) else None


        


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
            self.menu_page(user)
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
