from tkinter import *
from tkinter import Tk, font

root = Tk()
root.geometry("1500x1000")

label1 = Label(root, text="1")
label1.pack(side=BOTTOM)

label2 = Label(root, text="2")
label2.pack(side=BOTTOM)

label3 = Label(root, text="3")
label3.pack(side=BOTTOM)
root.mainloop()
