from tkinter import *
from tkinter import ttk
import time
import threading

def move(root):
    x,y=400,300
    time.sleep(1)
    for i in range(10):
        root.geometry(f"0x0+{x+10*i}+{y+10*i}")
        time.sleep(3)

root = Tk()
root.geometry("0x0+0+0")
# frm = ttk.Frame(root, padding=0)
# frm.grid()
# ttk.Label(frm, text="o").grid(column=0, row=0)
# ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
th = threading.Thread(target=move, args=(root,))
th.start()
root.mainloop()
