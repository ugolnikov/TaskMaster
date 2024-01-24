from tkinter import *
from tkinter import ttk
 
root = Tk()
root.title("TaskMaster - Меню")
root.geometry("213x399")
root.resizable(False, False)

root.iconbitmap("1.ico")
label_taskmaster = ttk.Label(text="TaskMaster", font = ("", 15))
label_taskmaster.pack(side=TOP, pady=10)

btn = ttk.Button(text="Список дел")
btn.pack(side=TOP, pady=3)
btn = ttk.Button(text="Друзья")
btn.pack(side=TOP, pady=3)
btn = ttk.Button(text="Настройки")
btn.pack(side=TOP, pady=3)

btn = ttk.Button(text="Выйти")
btn.pack(side=BOTTOM, pady=10)




 
 
root.mainloop()