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
        self.__EndDatum = IntVar()

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
        startdat_entry.grid(row=2,column=1)

        # Enddatum
        self.__enddat_entry = DateEntry(self, selectmode='day')
        self.__enddat_entry.grid(row=3,column=1)
        self.__enddat_entry.grid_remove()

        # Ansprechpartner
        display_an = ["Bitte Auswählen"]
        for ansprechpartner in range(len(self.__ansprechpartner)):
            display_an.append(self.__ansprechpartner[ansprechpartner][0])
        self.__ansprechpartner_sel = StringVar()
        self.__ansprechpartner_sel.set(display_an[0])
        ansprech_selec = OptionMenu(self, self.__ansprechpartner_sel, *display_an)
        ansprech_selec.grid(row=4, column=1)

        self.__ansprechpartner_sel.trace('w', self.__show_an_kcw)

        # Ansprechpartner KCW
        ansprechpartner_kcw = StringVar()
        ansprechpartner_kcw.set(display_an[0])
        self.__ansprech_kcw_selec = OptionMenu(self, ansprechpartner_kcw, *display_an)
        self.__ansprech_kcw_selec.grid(row=5, column=1)
        self.__ansprech_kcw_selec.grid_remove()

    def __show_an_kcw(self, *args):
        
        selected = self.__ansprechpartner_sel.get()
        ansprechpartner = [item[0] for item in self.__ansprechpartner]
        
        notkcw = not self.__ansprechpartner[ansprechpartner.index(selected)][3]

        if notkcw:
            self.__ansprech_kcw_selec.grid()
            self.__ansprechpartner_kcw_desc.grid()
        else:
            self.__ansprech_kcw_selec.grid_remove()
            self.__ansprechpartner_kcw_desc.grid_remove()


    def __editsparten(self):
        spartenwin = Editsparten(self, self.__currentsparten)

    def __editansprechpartner(self):
        pass

    def __makeenddat(self, *args):
        
        if self.__EndDatum.get():
            self.__enddat_entry.grid()
        else:
            self.__enddat_entry.grid_remove()

    
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

        sparten_edit_button = Button(self, text="bearbeiten", command=self.__editsparten)
        sparten_edit_button.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        # Calendar
        startdat_desc = Label(self, text="Startdatum:")
        startdat_desc.grid(row=2, column=0,padx=5,pady=5,sticky=W)

        enddat_desc = Checkbutton(self, text="Enddatum:", command=self.__makeenddat, variable=self.__EndDatum, onvalue=1,offvalue=0)
        enddat_desc.grid(row=3, column=0,padx=5,pady=5,sticky=W)

        # Ansprechpartner
        ansprechpartner_desc = Label(self, text='Ansprechpartner:')
        ansprechpartner_desc.grid(row=4,column=0,padx=5,pady=5,sticky=W)
        
        ansprechpartner_edit = Button(self, text="bearbeiten", command=self.__editansprechpartner)
        ansprechpartner_edit.grid(row=4,column=2,padx=5,pady=5,sticky=W)

        # Ansprechpartner KCW
        self.__ansprechpartner_kcw_desc = Label(self, text='Ansprechpartner KCW:')
        self.__ansprechpartner_kcw_desc.grid(row=5,column=0,padx=5,pady=5,sticky=W)
        self.__ansprechpartner_kcw_desc.grid_remove()

        # Save
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
editfahrten = EditFahrten(mainwin, sparten, fahrtenliste, ansprechpartner, 10)
mainwin.mainloop()