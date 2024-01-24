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
frame = tk.Frame(root)
frame.grid()
root.title("Главное меню")
root.geometry("200x300")
tk.Button(frame, text="Авторизация", command=lambda: goto("auth")).grid(column=1,row=0)
tk.Button(frame, text="Регистрация", command=root.destroy).grid(column=1,row=1)
tk.Button(frame, text="Выход", command=root.destroy).grid(column=1,row=2)




root.mainloop()