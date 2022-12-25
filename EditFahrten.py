import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import scrolledtext
from basicgui import *
from Editsparten import Editsparten
#from test import testsettings
from DateTime import *
import datetime
import tkcalendar
from tkcalendar import DateEntry
from TextEntry import TextEntry
from Ansprechpartner import Ansprechpartner

class EditFahrten(Toplevel):

    __fahrten = []
    __currentsparten = []
    __ansprechpartner = []
    __new = True
    __number = 0
    __desc_text = ""
    __item = []
    __delete_item = []

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

        self.__topwin = mainwin

        if self.__new:
            self.__desc_text = ""
        else:
            self.__desc_text = fahrtenliste[number]['Fließtext']

        #self.minsize(500, 300)
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
        fahrt_name_desc = Label(self, text="Fahrt Name*:")
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
        EndDatum = StringVar()
        self.__enddat_entry = DateEntry(self, selectmode='day', textvariable=EndDatum)
        self.__enddat_entry.grid(row=3,column=1)
        self.__enddat_entry.grid_remove()

        # Startzeit
        startzeit = StringVar()
        startzeit_entry = Entry(self, width=5, textvariable=startzeit)
        startzeit_entry.grid(row=4,column=1)

        # Endzeit
        endzeit = StringVar()
        endzeit_entry = Entry(self, width=5, textvariable=endzeit)
        endzeit_entry.grid(row=5,column=1)

        # Ansprechpartner
        display_an = ["Bitte Auswählen"]
        for ansprechpartner in range(len(self.__ansprechpartner)):
            display_an.append(self.__ansprechpartner[ansprechpartner][0])
        self.__ansprechpartner_sel = StringVar()
        self.__ansprechpartner_sel.set(display_an[0])
        ansprech_selec = OptionMenu(self, self.__ansprechpartner_sel, *display_an)
        ansprech_selec.grid(row=6, column=1)

        self.__ansprechpartner_sel.trace('w', self.__show_an_kcw)

        # Ansprechpartner KCW
        ansprechpartner_kcw = StringVar()
        ansprechpartner_kcw.set(display_an[0])
        self.__ansprech_kcw_selec = OptionMenu(self, ansprechpartner_kcw, *display_an)
        self.__ansprech_kcw_selec.grid(row=7, column=1)
        self.__ansprech_kcw_selec.grid_remove()

        # Save
        save = Button(self, text = "Speichern", command=lambda: self.__save(
            fahrt_insert.get(),
            sparte.get(),
            self.__StartDatum.get(),
            EndDatum.get(), 
            startzeit_entry.get(),
            endzeit_entry.get(),
            self.__ansprechpartner_sel.get(),
            ansprechpartner_kcw.get(),
            self.__desc_text,
            self.__item
            )
        )
        save.grid(row=500,column=1)

        

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
        Editsparten(self, self.__currentsparten)

    def __editansprechpartner(self):
        Ansprechpartner(self, self.__ansprechpartner)

    def __makeenddat(self, *args):
        
        if self.__EndDatum.get():
            self.__enddat_entry.grid()
        else:
            self.__enddat_entry.grid_remove()

    
    def __printwidgetsedit(self):

        # Fahrtname
        fahrt_name_desc = Label(self, text="Fahrt Name*:")
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
        sparte_desc = Label(self, text="Sparten Name*:")
        sparte_desc.grid(row=1, column=0,padx=5,pady=5,sticky=W)

        sparten_edit_button = Button(self, text="bearbeiten", command=self.__editsparten)
        sparten_edit_button.grid(row=1,column=2,padx=5,pady=5,sticky=W)

        # Calendar
        startdat_desc = Label(self, text="Startdatum*:")
        startdat_desc.grid(row=2, column=0,padx=5,pady=5,sticky=W)

        enddat_desc = Checkbutton(self, text="Enddatum:", command=self.__makeenddat, variable=self.__EndDatum, onvalue=1,offvalue=0)
        enddat_desc.grid(row=3, column=0,padx=5,pady=5,sticky=W)

        # Startzeit
        startzeit_desc = Label(self, text="Startzeit:")
        startzeit_desc.grid(row=4, column=0,padx=5,pady=5,sticky=W)

        startzeit_help = Label(self, text="Format: '00:00'")
        startzeit_help.grid(row=4, column=2,padx=5,pady=5,sticky=W)

        # Endzeit
        endzeit_desc = Label(self, text="Endzeit:")
        endzeit_desc.grid(row=5, column=0,padx=5,pady=5,sticky=W)

        endzeit_help = Label(self, text="Format: '00:00'")
        endzeit_help.grid(row=5, column=2,padx=5,pady=5,sticky=W)

        # Ansprechpartner
        ansprechpartner_desc = Label(self, text='Ansprechpartner*:')
        ansprechpartner_desc.grid(row=6,column=0,padx=5,pady=5,sticky=W)
        
        ansprechpartner_edit = Button(self, text="bearbeiten", command=self.__editansprechpartner)
        ansprechpartner_edit.grid(row=6,column=2,padx=5,pady=5,sticky=W)

        # Ansprechpartner KCW
        self.__ansprechpartner_kcw_desc = Label(self, text='Ansprechpartner KCW*:')
        self.__ansprechpartner_kcw_desc.grid(row=7,column=0,padx=5,pady=5,sticky=W)
        self.__ansprechpartner_kcw_desc.grid_remove()

        # Fließtext
        fließtext_desc = Label(self, text="Fließtext:")
        fließtext_desc.grid(row=8,column=0,padx=5,pady=5,sticky=W)

        fließtext_but = Button(self, text="bearbeiten", command=self.__fliesstextentry)
        fließtext_but.grid(row=8,column=2,padx=5,pady=5,sticky=W)

        # Items
        item_desc = Label(self, text="Stichpunkte:")
        item_desc.grid(row=9,column=0, padx=5,pady=5,sticky=W)

        item_add = Button(self, text="hinzufügen", command=self.__additem)
        item_add.grid(row=9, column=2,padx=5,pady=5,sticky=W)

        


    def __fliesstextentry(self):
        
        self.__fliesswin = Toplevel(self)
        self.__fliesswin.title("Text eingeben")

        self.__fliesswin.columnconfigure(0, weight =1)

        text_label = Label(self.__fliesswin, text="Bitte Text eingeben:")
        text_label.grid(column=0,row=0,padx=5,pady=5, sticky=W)

        text_entry = scrolledtext.ScrolledText(self.__fliesswin, wrap=tk.WORD, width=100, height=20)
        text_entry.grid(column=0,row=1,padx=5,pady=5, sticky=W)
        text_entry.insert(tk.END, self.__desc_text)

        save_bt = Button(self.__fliesswin, text="Speichern", command=lambda: self.__savefliesstext(text_entry))
        save_bt.grid(column=0,row=2)

        self.__fliesswin.mainloop()

    def __savefliesstext(self, textentry):

        self.__desc_text = textentry.get("1.0", tk.END)
        self.__fliesswin.destroy()


    def __additem(self):
        
        self.__item.append(Entry(self, width=70))
        self.__item[-1].grid(row=9+len(self.__item),column=0, columnspan=2,padx=5,pady=5, sticky=W)

        if len(self.__item)<2:
            self.__delbut = Button(self, text="löschen", command=self.__deleteitem)
            self.__delbut.grid(row=10,column=2,padx=5,pady=5, sticky=W)
        else:
            self.__delbut.grid_remove()
            self.__delbut.grid(row=9+len(self.__item), column=2,padx=5,pady=5, sticky=W)

    def __deleteitem(self):

        self.__item[-1].grid_remove()
        self.__item.pop()

        if len(self.__item)>0:
            self.__delbut.grid_remove()
            self.__delbut.grid(column=2, row=9+len(self.__item),padx=5,pady=5, sticky=W)
        else:
            self.__delbut.grid_remove()


    def __save(self, fahrtname, spartenname, startdatum, enddatum, startzeit, endzeit, ansprechpartner, ansprechpartnerkcw,fliesstext, stichpunkte, number=None):

        ansprechpartner_kcw_needed = False
        # Conversion
        spartenname = spartenname[4:]
        start_year = int("20"+startdatum[-2:])
        if startdatum[3] == "0":
            start_month = int(startdatum[4])
        else:
            start_month = int(startdatum[3:5])
        if startdatum[0] == '0':
            start_day = int(startdatum[1])
        else:
            start_day = int(startdatum[:2])
        startdatum = datetime.date(year=start_year, month=start_month, day=start_day)

        if self.__EndDatum.get():
            end_year = int("20"+enddatum[-2:])
            if enddatum[3] == "0":
                end_month = int(enddatum[4])
            else:
                end_month = int(enddatum[3:5])
            if enddatum[0] == '0':
                end_day = int(enddatum[1])
            else:
                end_day = int(enddatum[:2])
            enddatum = datetime.date(year=end_year, month=end_month, day=end_day)
        else:
            enddatum = None

       

        ansprechpartner_namen = [name[0] for name in self.__ansprechpartner]

        if ansprechpartner not in ansprechpartner_namen:
            msgbox.showwarning("Eingabe falsch", "Bitte Ansprechpartner auswählen")
            return 0
        
        ansprechpartner_i = ansprechpartner_namen.index(ansprechpartner)
        
        if not self.__ansprechpartner[ansprechpartner_i][3]:
            
            if ansprechpartnerkcw not in ansprechpartner_namen:
                msgbox.showwarning("Eingabe falsch", "Bitte KCW Ansprechpartner auswählen")
                return 0

            ansprechpartner_kcw_i = ansprechpartner_namen.index(ansprechpartnerkcw)
            ansprechpartner_kcw_needed = True
        
        # Errors

        if spartenname not in self.__currentsparten:
            msgbox.showwarning("Eingabe falsch", "Bitte Sparte auswählen")
            return 0

        if self.__EndDatum.get() and startdatum>enddatum:
            msgbox.showwarning("Eingabe falsch", "Enddatum kann nicht vor Startdatum liegen")
            return 0

        if (not fahrtname):
            msgbox.showwarning("Eingabe falsch", "Fahrt Name fehlt")
            return 0
        
        
        spartennr = self.__currentsparten.index(spartenname)
        # Save
        stichpunkte_save = []
        for stichpunkt in stichpunkte:
            stichpunkte_save.append(stichpunkt.get())

        if (not number) and ansprechpartner_kcw_needed:
            appenddictionarylist(
                liste = self.__fahrten,
                inSparte = spartenname,
                inFahrtname = fahrtname,
                inSpartennr = spartennr,
                inStartDatum = startdatum,
                inEndDatum = enddatum,
                inAnsprechpartner = self.__ansprechpartner[ansprechpartner_i],
                inAnsprechpartnerKCW=self.__ansprechpartner[ansprechpartner_kcw_i],
                inItems = stichpunkte_save
            )
            self.__topwin.printfahrten()
            self.destroy()
        elif not number:
            appenddictionarylist(
                liste = self.__fahrten,
                inSparte = spartenname,
                inFahrtname = fahrtname,
                inSpartennr = spartennr,
                inStartDatum = startdatum,
                inEndDatum = enddatum,
                inAnsprechpartner = self.__ansprechpartner[ansprechpartner_i],
                inItems = stichpunkte_save
            )
            self.__topwin.printfahrten()
            self.destroy()
        else:
            pass
            # change existing dict



#Test
class Mainwin(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(350, 200)
        self.main_frame = tk.Frame(self)
        self.user_info_label = tk.Label(self)
        self.wm_title("Test")
        

def appenddictionarylist(liste, inSparte, inSpartennr, inStartDatum, inAnsprechpartner, inItems, inFahrtname, inFließtext=None,inAnsprechpartnerKCW=None, inEndDatum=None, inStartzeit=None, inEndzeit=None):
    liste.append({
        'Sparte' : inSparte,
        'Spartennr' : inSpartennr,
        'Fahrtname' : inFahrtname,
        'Startzeit' : inStartzeit,
        'Endzeit' : inEndzeit,
        'StartDatum' : inStartDatum,
        'EndDatum' : inEndDatum,
        'Ansprechpartner' : inAnsprechpartner, # 2D-Liste mit Ansprechpartner, Email. Wenn Länge>1: Ansprechpartner, Ansprechpartner KCW, Ansprechpartner n
        'AnsprechpartnerKCW' : inAnsprechpartnerKCW,
        'Fließtext' : inFließtext,
        'items' : inItems # Liste mit Stichpunkten
    })
