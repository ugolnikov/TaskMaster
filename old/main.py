import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from PIL import Image, ImageTk
from tkinter import filedialog

class CardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Карточки с вопросами")
        self.root.geometry("800x400")

        self.current_user = None
        self.current_user_image_path = None

        # Создание базы данных и таблицы пользователей
        self.conn = sqlite3.connect("accounts.db")
        self.create_users_table()

        # Создание интерфейса для авторизации
        self.create_login_window()

    def create_users_table(self):
        # Создание таблицы пользователей, если она не существует
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            image_path TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def create_notes_table(self):
        # Создание таблицы заметок для текущего пользователя, если она не существует
        query = f'''
        CREATE TABLE IF NOT EXISTS {self.current_user}_notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT NOT NULL,
            image_path TEXT
        )
        '''
        self.conn.execute(query)
        self.conn.commit()

    def create_login_window(self):
        # Элементы интерфейса для авторизации
        self.label_login_username = tk.Label(self.root, text="Имя пользователя:")
        self.label_login_password = tk.Label(self.root, text="Пароль:")
        self.entry_login_username = tk.Entry(self.root)
        self.entry_login_password = tk.Entry(self.root, show="*")
        self.btn_login = tk.Button(self.root, text="Вход", command=self.login_user)
        self.btn_register = tk.Button(self.root, text="Регистрация", command=self.register_user)

        # Упаковка элементов на форму
        self.label_login_username.grid(row=0, column=0)
        self.label_login_password.grid(row=1, column=0)
        self.entry_login_username.grid(row=0, column=1)
        self.entry_login_password.grid(row=1, column=1)
        self.btn_login.grid(row=2, column=0, columnspan=2)
        self.btn_register.grid(row=3, column=0, columnspan=2)

    def create_main_window(self):
        # Элементы интерфейса для работы с заметками
        self.label_note = tk.Label(self.root, text="Заметка:")
        self.entry_note = tk.Entry(self.root)
        self.btn_add_note = tk.Button(self.root, text="Добавить заметку", command=self.add_note)
        self.btn_load_notes = tk.Button(self.root, text="Загрузить заметки", command=self.load_notes)
        self.note_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE)
        self.btn_delete_note = tk.Button(self.root, text="Удалить заметку", command=self.delete_note)
        self.btn_edit_note = tk.Button(self.root, text="Изменить заметку", command=self.edit_note)
        self.btn_browse_image = tk.Button(self.root, text="Изменить изображение", command=self.browse_image)
        self.image_label = tk.Label(self.root)

        # Упаковка элементов на форму
        self.label_note.grid(row=0, column=2)
        self.entry_note.grid(row=0, column=3)
        self.btn_add_note.grid(row=1, column=2, columnspan=2)
        self.btn_load_notes.grid(row=2, column=2, columnspan=2)
        self.note_listbox.grid(row=3, column=2, rowspan=5, columnspan=2, sticky=tk.N+tk.S)
        self.btn_delete_note.grid(row=8, column=2, columnspan=2, sticky=tk.W+tk.E)
        self.btn_edit_note.grid(row=9, column=2, columnspan=2, sticky=tk.W+tk.E)
        self.btn_browse_image.grid(row=10, column=2, columnspan=2)
        self.image_label.grid(row=3, column=4, rowspan=5, columnspan=2, sticky=tk.N+tk.S)

        # Отображение изображения пользователя
        if self.current_user_image_path:
            self.display_user_image()

    def login_user(self):
        username = self.entry_login_username.get()
        password = self.entry_login_password.get()

        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        # Проверка существования пользователя и правильности пароля
        user = self.conn.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password)).fetchone()

        if user:
            self.current_user = username
            self.current_user_image_path = user[3]  # Получаем путь к изображению из базы данных
            self.create_notes_table()
            self.root.destroy()  # Закрыть окно авторизации
            self.root = tk.Tk()  # Создать новое окно для основного интерфейса
            self.root.title("Карточки с вопросами")
            self.root.geometry("800x400")
            self.create_main_window()
            self.load_notes()  # Загрузить заметки при входе в аккаунт
        else:
            messagebox.showerror("Ошибка", "Неправильное имя пользователя или пароль")

    def register_user(self):
        username = simpledialog.askstring("Регистрация", "Введите имя пользователя:")
        password = simpledialog.askstring("Регистрация", "Введите пароль:", show="*")

        if not username or not password:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        # Выбор изображения при регистрации
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        # Регистрация нового пользователя
        self.conn.execute("INSERT INTO users (username, password, image_path) VALUES (?, ?, ?)", (username, password, file_path))
        self.conn.commit()
        messagebox.showinfo("Успех", "Регистрация успешна")

    def add_note(self):
        if not self.current_user:
            messagebox.showerror("Ошибка", "Вы не авторизованы")
            return

        note_text = self.entry_note.get()

        if not note_text:
            messagebox.showerror("Ошибка", "Введите текст заметки")
            return

        # Добавление заметки в базу данных
        self.create_notes_table()  # Убедимся, что таблица существует
        self.conn.execute(f"INSERT INTO {self.current_user}_notes (note) VALUES (?)", (note_text,))
        self.conn.commit()
        self.load_notes()  # Перезагрузка списка заметок

    def load_notes(self):
        if not self.current_user:
            messagebox.showerror("Ошибка", "Вы не авторизованы")
            return

        # Очистка списка заметок перед загрузкой
        self.note_listbox.delete(0, tk.END)

        # Загрузка заметок текущего пользователя из базы данных
        notes = self.conn.execute(f"SELECT * FROM {self.current_user}_notes").fetchall()

        for note in notes:
            self.note_listbox.insert(tk.END, note[1])

    def delete_note(self):
        if not self.current_user:
            messagebox.showerror("Ошибка", "Вы не авторизованы")
            return

        # Получаем выделенную заметку в списке
        selected_index = self.note_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Ошибка", "Выберите заметку для удаления")
            return

        # Удаляем заметку из базы данных
        note_text = self.note_listbox.get(selected_index)
        self.conn.execute(f"DELETE FROM {self.current_user}_notes WHERE note=?", (note_text,))
        self.conn.commit()
        self.load_notes()  # Перезагрузка списка заметок

    def edit_note(self):
        if not self.current_user:
            messagebox.showerror("Ошибка", "Вы не авторизованы")
            return

        # Получаем выделенную заметку в списке
        selected_index = self.note_listbox.curselection()

        if not selected_index:
            messagebox.showerror("Ошибка", "Выберите заметку для изменения")
            return

        # Открываем диалоговое окно для изменения заметки
        new_text = simpledialog.askstring("Изменение заметки", "Введите новый текст заметки:", initialvalue=self.note_listbox.get(selected_index))

        if new_text is not None:
            # Обновляем заметку в базе данных
            old_text = self.note_listbox.get(selected_index)
            self.conn.execute(f"UPDATE {self.current_user}_notes SET note=? WHERE note=?", (new_text, old_text))
            self.conn.commit()
            self.load_notes()  # Перезагрузка списка заметок

    def browse_image(self):
        if not self.current_user:
            messagebox.showerror("Ошибка", "Вы не авторизованы")
            return

        # Выбор нового изображения и его отображение на форме
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.current_user_image_path = file_path
            self.display_user_image()
            # Обновление пути к изображению в базе данных
            self.conn.execute("UPDATE users SET image_path=? WHERE username=?", (file_path, self.current_user))
            self.conn.commit()

    def display_user_image(self):
        if self.current_user_image_path:
            # Отображение изображения пользователя
            image = Image.open(self.current_user_image_path)
            image = image.resize((100, 100), Image.ANTIALIAS if hasattr(Image, "ANTIALIAS") else Image.BICUBIC)
            photo = ImageTk.PhotoImage(image)
            self.image_label.config(image=photo)
            self.image_label.image = photo

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = CardApp(root)
    app.run()
