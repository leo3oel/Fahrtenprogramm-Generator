import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from basicgui import *
from Editsparten import *
from test import testsettings

class EditFahrten(Toplevel):

    __fahrten = []
    __currentsparten = []
    __ansprechpartner = []
    __new = False
    __number = 0

    def __init__(self, mainwin, sparten, fahrtenliste, ansprechpartnerliste, number):

        Toplevel.__init__(self, mainwin)
        
        self.__currentsparten = sparten
        self.__fahrtenliste = fahrtenliste
        self.__ansprechpartner = ansprechpartnerliste
        self.__number = number

        if self.__number>(len(self.__fahrten)-1):
            self.title("Fahrt hinzufügen")
            self.__new = True
        else:
            self.title("Fahrt bearbeiten")
            self.__new = False

        self.__makewindow()
        self.mainloop()

    def __makewindow(self):

        self.minsize(500, 300)
        
        self.columnconfigure(0, weight =2) # Description
        self.columnconfigure(1, weight =1) # Enter Value/Select
        self.columnconfigure(2, weight =1) # Only for calendar

        self.__printwidgets()

    def __printwidgets(self):
        fahrt_name_desc = Label(self, text="Fahrt Name:")
        fahrt_name_desc.grid(row=0, column=0,padx=5,pady=5,sticky=W)

        if self.__new:
            fahrt_name = StringVar()
            fahrt_name = self.__fahrten[self.__number]['Fahrtname']
        else:
            fahrt_name = StringVar()

        fahrt_insert = Entry(self, width=50, textvariable=fahrt_name)
        fahrt_insert.insert(0, self.__fahrten[self.__number]['Fahrtname'])
        fahrt_insert.grid(row=0, column=1, padx=5,pady=5,sticky=E)
        
        save = Button(self, text = "Speichern")
        save.grid(row=50,column=1)




class Mainwin(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(350, 200)
        self.main_frame = tk.Frame(self)
        self.user_info_label = tk.Label(self)
        self.wm_title("Test")
        

mainwin = Mainwin()
ansprechpartner, fahrtenliste, sparten = testsettings()
editfahrten = EditFahrten(mainwin, sparten, fahrtenliste, ansprechpartner, 0)
mainwin.mainloop()