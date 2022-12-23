import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from basicgui import *
from test import Mainwin

class Editsparten(Toplevel):

    __currentsparten = []

    def __init__(self, mainwin, sparten):

        Toplevel.__init__(self, mainwin)
        self.title("Sparten bearbeiten")
        self.__currentsparten = sparten
        self.__makewindow()
        
        self.protocol("WM_DELETE_WINDOW", mainwin.makewindow)
        self.mainloop()

    def __makewindow(self):

        self.minsize(350, 200)
        
        self.columnconfigure(0, weight =1) # Startdatum
        self.columnconfigure(1, weight =1) # Enddatum
        self.columnconfigure(2, weight =1) # Sparte

        self.__printwidgets()


    def __printwidgets(self):
        
        for widget in self.winfo_children(): # destroy all widgets
            widget.destroy()

        spartennr_label = []
        spartenname_label = []
        delete_buttons = []

        spartennr_label.append(Label(self, text="Spartennummer"))
        spartennr_label[0].grid(column=0,row=0,padx=5,pady=5, sticky=W)

        spartenname_label.append(Label(self, text="Spartename")) 
        spartenname_label[0].grid(column=1,row=0,padx=5,pady=5, sticky=W)


        delete_buttons.append(Button(self, text="Sparte hinzufügen", command=self.__callAddSparte))
        delete_buttons[0].grid(column=2, row=0,pady=5,padx=5,sticky=W)

        hline(self, 1,3)

        for increment in range(len(self.__currentsparten)):
            
            spartennr_label.append(Label(self, text=str(increment+1)))
            spartennr_label[increment+1].grid(column=0, row=increment+2,pady=5,padx=5,sticky=W)

            spartenname_label.append(Label(self, text=self.__currentsparten[increment]))
            spartenname_label[increment+1].grid(column=1, row=increment+2,pady=5,padx=5,sticky=W)

            delete_buttons.append(Button(self, text="Sparte loeschen", command=lambda c=increment: self.__deletesparte(c)))
            delete_buttons[increment+1].grid(column=2, row=increment+2,pady=5,padx=5,sticky=W)


    def __deletesparte(self, number):
        self.__currentsparten.pop(number)
        self.__printwidgets()
        self.update()

    def __callAddSparte(self):
        addspartewin = AddSparte(self, self.__currentsparten)
        self.__printwidgets()


class AddSparte(Toplevel):

    __currentsparten = []

    def __init__(self, mainwin, sparten):

        Toplevel.__init__(self, mainwin)
        self.title("Sparten hinzufügen")
        self.__currentsparten = sparten
        self.__makewindow()
        

        self.mainloop()

    def __makewindow(self):
        self.minsize(350, 200)
        
        self.columnconfigure(0, weight =1) # Startdatum
        self.columnconfigure(1, weight =1) # Enddatum

        self.__printwidgets()

    def __printwidgets(self):

        sparten_name_label = Label(self, text="Sparten Name:")
        sparten_name_label.grid(row=0, column=0, padx=5,pady=5,sticky=W)

        sparten_name_entry = Entry(self, width=50)
        sparten_name_entry.grid(row=0, column=1, padx=5,pady=5,sticky=E)

        sparten_nr_label = Label(self, text="Sparten Nr:")
        sparten_nr_label.grid(row=1, column=0, padx=5,pady=5,sticky=W)

        listlength = len(self.__currentsparten)+1

        if listlength>1:
            sparten_nr_spinbox = Spinbox(self, from_= 1, to=listlength)
            sparten_nr_spinbox.grid(row=1,column=1, padx=5,pady=5,sticky=W)
        else:
            sparten_nr_label2 = Label(self, text="1")
            sparten_nr_label2.grid(row=1,column=1, padx=5,pady=5,sticky=W)
            sparten_nr_spinbox = 1

        

        save_button = Button(self, text="Speichern", command=lambda: self.__save(sparten_name_entry, sparten_nr_spinbox))
        save_button.grid(row=2,column=1, padx=5,pady=5,sticky=W)

    def __save(self, sparten_name_e, sparten_nr_e):
        
        sparten_name = sparten_name_e.get()
        if sparten_nr_e == 1:
            sparten_nr = 0
        else:
            sparten_nr = int(sparten_nr_e.get())-1

        if (sparten_nr <0) or (sparten_nr>len(self.__currentsparten)):
            msgbox.showwarning("Eingabe falsch", "Bitte richtige Nummer eingeben")
            return 0

        if sparten_name:
            self.__currentsparten.insert(sparten_nr, sparten_name)
            self.quit()
        else:
            msgbox.showwarning("Eingabe unvollständig", "Bitte Spartenname eingeben")

        

""" mainwin = Mainwin()
sparten = ["Kanupolo", "Allgemein", "idk"]
Editsparten(mainwin, sparten)
mainwin.mainloop() """