
from TeXport import 
from tkinter import *
from tkinter import ttk

def hline(win, inrow, width):
    for i in range(width):
        ttk.Separator(master=win, orient=HORIZONTAL).grid(row=inrow, column=i,sticky="ew")

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

def deletesparte(win, sparten,number):
    sparten.pop(number)
    printsparten(win, sparten)
    win.update()


def editsparten(add, sparten):
    
    spartewin=Toplevel(add)
    spartewin.title("Sparten bearbeiten")
    spartewin.geometry('480x270')
    
    spartewin.columnconfigure(0, weight =1) # Startdatum
    spartewin.columnconfigure(1, weight =1) # Enddatum
    spartewin.columnconfigure(2, weight =1) # Sparte

    printsparten(spartewin, sparten)




""" def getsparte(choice):
    #choice = variable.get()
    spartennr = int(choice[0])-1
    spartenname = str(choice[4:])
    return(spartenname)
 """

def printsparten(win, sparten):

    for widget in win.winfo_children(): # destroy all widgets
        widget.destroy()

    spartennr_label = []
    spartenname_label = []
    delete_buttons = []

    spartennr_label.append(Label(win, text="Spartennummer"))
    spartennr_label[0].grid(column=0,row=0,padx=5,pady=5, sticky=W)

    spartenname_label.append(Label(win, text="Spartename")) 
    spartenname_label[0].grid(column=1,row=0,padx=5,pady=5, sticky=W)

    hline(win, 1,3)

    for increment in range(len(sparten)):
        
        spartennr_label.append(Label(win, text=str(increment+1)))
        spartennr_label[increment+1].grid(column=0, row=increment+2,pady=5,padx=5,sticky=W)

        spartenname_label.append(Label(win, text=sparten[increment]))
        spartenname_label[increment+1].grid(column=1, row=increment+2,pady=5,padx=5,sticky=W)

        delete_buttons.append(Button(win, text="Sparte loeschen", command=lambda c=increment: deletesparte(win, sparten, c)))
        delete_buttons[increment].grid(column=2, row=increment+2,pady=5,padx=5,sticky=W)

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

    sparten = ["Allgemein", 'Jugend']

    displaysparten = ["0 - Bitte Auswählen"]
    for sparte in range(len(sparten)):
        displaysparten.append(str(sparte+1) + " - " + sparten[1])

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