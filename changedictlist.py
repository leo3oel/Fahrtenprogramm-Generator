import tkinter.messagebox
from TeXport import appenddictionarylist
from tkinter import *

def savefahrt(terminedic, fahrt_insert, sparte_insert, spartenr_insert, ansprechpart_insert, ansprechpartkcw_insert, startdatum_insert, startzeit_insert, enddatum_insert, endzeit_insert, fahrtname_insert, fließtext_insert, items_insert):
    
    fahrtname = fahrt_insert.get()
    sparte = sparte_insert.get()
    spartennr = spartenr_insert.get()
    ansprechpartner = ansprechpart_insert.get()
    ansprechpartnerKCW = ansprechpartkcw_insert.get()
    startdatum = startdatum_insert.get()
    startzeit = startzeit_insert.get()
    enddatum = enddatum_insert.get()
    endzeit = endzeit_insert.get()
    fließtext = fließtext_insert.get()
    items = items_insert.get()

    if not fahrtname:
        tkinter.messagebox.showinfo("Wert fehlt","Der Wert Fahrtname fehlt")
        return 0
    
    appenddictionarylist(
        liste=terminedic,
        inSparte=sparte,
        inSpartennr=spartennr,
        inAnsprechpartner=ansprechpartner,
        inAnsprechpartnerKCW=ansprechpartnerKCW,
        inStartDatum=startdatum,
        inStartzeit=startzeit,
        inEndDatum=enddatum,
        inEndzeit=endzeit,
        inFahrtname=fahrtname,
        inFließtext=fließtext,
        inItems=items
    )

def addfahrt(terminedic, mainwin):
    add=Toplevel(mainwin)
    add.title("Fahrt bearbeiten")
    add.geometry('960x540')
    
    # 3 columns
    add.columnconfigure(0, weight =2) # Description
    add.columnconfigure(1, weight =1) # Enter Value/Select
    add.columnconfigure(2, weight =1) # Only for calendar

    
    fahrt_name_desc = Label(add, text="Fahrt Name:")
    fahrt_name_desc.grid(row=0, column=0,padx=5,pady=5,sticky=W)

    fahrt_name = ""
    fahrt_insert = Entry(add, width=50, textvariable=fahrt_name)
    fahrt_insert.grid(row=0, column=1, padx=5,pady=5,sticky=E)

    # Dropdown Sparten Select

    # Calendar Date Select

    # Time Select (maybe with clock)

    # Ansprechpartner select

    # Optional: Texteingabe -> extra window

    # Items Eingabe
    
    save = Button(add, text = "Speichern")#, command=lambda: savefahrt())
    save.grid(row=50,column=1)

    add.mainloop()