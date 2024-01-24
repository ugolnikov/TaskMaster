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
root.geometry("400x300")





root.mainloop()