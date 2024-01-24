import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
from tkinter import filedialog
from sqlalchemy import column

def goto(module_name):
    root.destroy()
    import importlib
    mod = importlib.import_module(module_name)
    

root = tk.Tk()
root.iconbitmap("1.ico")
frame = tk.Frame(root)
frame.pack()
root.title("Главное меню")
root.geometry("200x300")
tk.Button(frame, text="Авторизация", command=lambda: goto("auth")).pack(side="top",fill="x", pady=30)
tk.Button(frame, text="Регистрация", command=lambda: goto("register")).pack(side="top",fill="x", pady=30)
tk.Button(frame, text="Выход", command=root.destroy).pack(side="top",fill="x", pady=30)




root.mainloop()