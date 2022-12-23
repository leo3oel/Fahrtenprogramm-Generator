import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from basicgui import *
from Editsparten import Editsparten
from test import testsettings
from DateTime import *
import tkcalendar
from tkcalendar import DateEntry

class EditFahrten(Toplevel):

    __fahrten = []
    __currentsparten = []
    __ansprechpartner = []
    __new = True
    __number = 0

    def __init__(self, mainwin, sparten, fahrtenliste, ansprechpartnerliste, number):

        Toplevel.__init__(self, mainwin)
        
        self.__currentsparten = sparten
        self.__fahrten = fahrtenliste
        self.__ansprechpartner = ansprechpartnerliste
        self.__number = number

        if self.__number>(len(self.__fahrten)-1):
            self.title("Fahrt hinzufügen")
            self.__new = True
        else:
            self.title("Fahrt bearbeiten")
            self.__new = False

        self.__StartDatum = StringVar()
        self.__EndDatum = StringVar()

        self.minsize(500, 300)
        self.makewindow()
        self.mainloop()


    def makewindow(self):

        for widget in self.winfo_children(): # destroy all widgets
            widget.destroy()

        self.columnconfigure(0, weight =2) # Description
        self.columnconfigure(1, weight =1) # Enter Value/Select
        self.columnconfigure(2, weight =1) # Only for calendar

        if self.__new:
            self.__printwidgetsnew()
        else:
            self.__printwidgetsedit()

        self.__printwidgetsgeneral()


    def __printwidgetsnew(self):
        
        # Fahrtname
        fahrt_name_desc = Label(self, text="Fahrt Name:")
        fahrt_name_desc.grid(row=0, column=0,padx=5,pady=5,sticky=W)

        fahrt_name = StringVar()
        fahrt_insert = Entry(self, width=50, textvariable=fahrt_name)

        fahrt_insert.grid(row=0, column=1, padx=5,pady=5,sticky=E)

        # Sparten
        displaysparten = ["0 - Bitte Auswählen"]
        for sparte in range(len(self.__currentsparten)):
            displaysparten.append(str(sparte+1) + " - " + self.__currentsparten[sparte])

        sparte = StringVar()
        sparte.set(displaysparten[0])
        sparten_selec = OptionMenu(self, sparte, *displaysparten)#, command=getsparte)
        sparten_selec.grid(row=1, column=1)

        # Startdatum
        startdat_entry = DateEntry(self, selectmode='day', textvariable=self.__StartDatum)
        startdat_entry.grid(row=2,column=2)

        #self.__StartDatum.trace('w', self.__selectenddatum)
        # Enddatum
        
        

        self.__StartDatum.trace('w', lambda var_name, var_index, operation: self.__makeenddat(startdat_entry))

    def __editsparten(self):
        spartenwin = Editsparten(self, self.__currentsparten)
    
    def __makeenddat(self, startddat):
        #https://stackoverflow.com/questions/66510020/select-date-range-with-tkinter
        self.__StartDatum = startddat.get_date()
        enddat_entry = DateEntry(self, selectmode='day')
        enddat_entry.set_date(self.__StartDatum)
        enddat_entry.grid(row=3,column=2)

    def __printwidgetsedit(self):

        # Fahrtname
        fahrt_name_desc = Label(self, text="Fahrt Name:")
        fahrt_name_desc.grid(row=0, column=0,padx=5,pady=5,sticky=W)

        fahrt_name = StringVar()
        fahrt_name = self.__fahrten[self.__number]['Fahrtname']
        fahrt_insert = Entry(self, width=50, textvariable=fahrt_name)
        fahrt_insert.delete(0, "end")
        fahrt_insert.insert(0, self.__fahrten[self.__number]['Fahrtname'])
        fahrt_insert.grid(row=0, column=1, padx=5,pady=5,sticky=E)

        # Sparten
        displaysparten = ["0 - Bitte Auswählen"]
        for sparte in range(len(self.__currentsparten)):
            displaysparten.append(str(sparte+1) + " - " + self.__currentsparten[sparte])

        sparte = StringVar()
        sparte.set(displaysparten[self.__fahrten[self.__number]["Spartennr"]+1])
        sparten_selec = OptionMenu(self, sparte, *displaysparten)#, command=getsparte)
        sparten_selec.grid(row=1, column=1)


        # print Date
        



    def __printwidgetsgeneral(self):

        # Sparten Name Eingabe
        sparte_desc = Label(self, text="Sparten Name:")
        sparte_desc.grid(row=1, column=0,padx=5,pady=5,sticky=W)

        
        # Sparten bearbeiten
        sparten_edit_button = Button(self, text="Sparten bearbeiten", command=self.__editsparten)
        sparten_edit_button.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        # Calendar
        startdat_desc = Label(self, text="Startdatum:")
        startdat_desc.grid(row=2, column=0,padx=5,pady=5,sticky=W)

        #startdat_edit_button = Button(self, text="Datum bearbeiten", command=self.__editdate)
        #startdat_edit_button.grid(row=2,column=2, padx=5,pady=5,sticky=W)

        enddat_desc = Label(self, text="Enddatum:")
        enddat_desc.grid(row=3, column=0,padx=5,pady=5,sticky=W)

        #enddat_edit_button = Button(self, text="Datum bearbeiten", command=self.__editdate)
        #enddat_edit_button.grid(row=3,column=2, padx=5,pady=5,sticky=W)

        # Save
        save = Button(self, text = "Speichern")
        save.grid(row=50,column=1)


    def __editdate(self):
        pass


class Mainwin(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(350, 200)
        self.main_frame = tk.Frame(self)
        self.user_info_label = tk.Label(self)
        self.wm_title("Test")
        

mainwin = Mainwin()
ansprechpartner, fahrtenliste, sparten = testsettings()
editfahrten = EditFahrten(mainwin, sparten, fahrtenliste, ansprechpartner, 10)
mainwin.mainloop()