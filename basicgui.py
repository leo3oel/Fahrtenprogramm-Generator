from tkinter import ttk
from tkinter import *


def hline(win, inrow, width):
    for i in range(width):
        ttk.Separator(master=win, orient=HORIZONTAL).grid(row=inrow, column=i,sticky="ew")