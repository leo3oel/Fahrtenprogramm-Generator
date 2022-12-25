import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from basicgui import *
from tkinter import scrolledtext

class TextEntry(Toplevel):
    def __init__(self, mainwin, text):

        Toplevel.__init__(self, mainwin)
        self.title("Text eingeben")
        self.__text = text
        self.__makewindow()
        
        self.protocol("WM_DELETE_WINDOW", self.__save)
        self.__topwin = mainwin


        self.mainloop()

    def __makewindow(self):
        
        self.columnconfigure(0, weight =1) # Startdatum

        self.__printwidgets()

    def __printwidgets(self):
        
        text_label = Label(self, text="Bitte Text eingeben:")
        text_label.grid(column=0,row=0,padx=5,pady=5, sticky=W)

        self.__text_entry = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=100, height=20)
        self.__text_entry.grid(column=0,row=1,padx=5,pady=5, sticky=W)
        self.__text_entry.insert(tk.END, self.__text)

    def __save(self):
        
        self.__topwin.desc_text = self.__text
        self.destroy()
