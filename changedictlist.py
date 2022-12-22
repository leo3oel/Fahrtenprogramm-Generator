import tkinter.messagebox
from TeXport import appenddictionarylist
from tkinter import *
from gui import hline

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


def addsparte():
    print(0)

def editsparten(add, sparten):
    
    spartewin=Toplevel(add)
    spartewin.title("Sparten bearbeiten")
    spartewin.geometry('480x270')
    
    # Menubar
    mn = Menu(spartewin) 
    spartewin.config(menu=mn) 
    
    mn.add_command(label = "Sparte hinzufügen", command=addsparte)

    spartennr_label = []
    spartenname_label = []

    spartennr_label.append(Label(spartewin, text="Spartennummer"))
    spartennr_label[0].grid(column=0,row=0,padx=5,pady=5, sticky=W)

    spartenname_label.append(Label(spartewin, text="Spartename")) 
    spartennr_label[0].grid(column=1,row=0,padx=5,pady=5, sticky=W)

    hline(1,2)

    

    spartewin.mainloop()




""" def getsparte(choice):
    #choice = variable.get()
    spartennr = int(choice[0])-1
    spartenname = str(choice[4:])
    return(spartenname)
 """


def addfahrt(terminedic, mainwin, sparten):
    add=Toplevel(mainwin)
    add.title("Fahrt bearbeiten")
    add.geometry('960x540')
    
    # 3 columns
    add.columnconfigure(0, weight =2) # Description
    add.columnconfigure(1, weight =1) # Enter Value/Select
    add.columnconfigure(2, weight =1) # Only for calendar

    # Fahrt Name Eingabe
    fahrt_name_desc = Label(add, text="Fahrt Name:")
    fahrt_name_desc.grid(row=0, column=0,padx=5,pady=5,sticky=W)

    fahrt_name = ""
    fahrt_insert = Entry(add, width=50, textvariable=fahrt_name)
    fahrt_insert.grid(row=0, column=1, padx=5,pady=5,sticky=E)

    # Sparten Name Eingabe
    sparte_desc = Label(add, text="Fahrt Name:")
    sparte_desc.grid(row=1, column=0,padx=5,pady=5,sticky=W)

    sparten = [[1, "Allgemein"], [2, "Jugend"]]

    displaysparten = ["0 - Bitte Auswählen"]
    for sparte in sparten:
        displaysparten.append(str(sparte[0]) + " - " + sparte[1])

    sparte = StringVar()
    sparte.set(displaysparten[0])
    sparten_selec = OptionMenu(add, sparte, *displaysparten)#, command=getsparte)
    sparten_selec.grid(row=1, column=1)

    # Sparten bearbeiten
    sparten_edit_button = Button(add, text="Sparten bearbeiten", command=lambda: editsparten(add, sparten))
    sparten_edit_button.grid(row=1,column=2)

    # Calendar Date Select

    # Time Select (maybe with clock)

    # Ansprechpartner select

    # Optional: Texteingabe -> extra window

    # Items Eingabe
    
    save = Button(add, text = "Speichern", command=lambda: print(sparte.get()))#savefahrt())
    save.grid(row=50,column=1)

    add.mainloop()