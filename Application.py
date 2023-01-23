import tkinter
from tkinter import *
import csv
import os

def AppStart():
    start.destroy()
    os.system("python Manager.py")

start = tkinter.Tk()
start.geometry('%dx%d' % (600, 600))

bar = tkinter.Frame(start, bd=3)
bar.grid_rowconfigure(0, weight=2)
bar.grid_columnconfigure(0, weight=2)

with open('Application.csv', 'r') as file:
    r = csv.reader(file)
    next(r, None)
    lines = [line for line in r]

canvas = tkinter.Canvas(bar, bd=0)
canvas.config(width=300, height=300)
btn = Button(canvas, text="Manager", command=lambda:AppStart())
btn.place(relx=0.75, rely=0.5)
bar.pack()
start.mainloop()


