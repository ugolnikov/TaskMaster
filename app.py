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
root.title("Меню")
root.geometry("220x300")
tk.Label(frame, text="TaskMaster", fg="black", background="white").pack(side="top",fill="x",pady=10)
tk.Button(frame, text="Авторизация", command=lambda: goto("auth")).pack(side="top",fill="x", pady=30)
tk.Button(frame, text="Регистрация", command=lambda: goto("register")).pack(side="top",fill="x", pady=20)
tk.Button(frame, text="Выход", command=root.destroy).pack(side="top",fill="x", pady=20)




root.mainloop()