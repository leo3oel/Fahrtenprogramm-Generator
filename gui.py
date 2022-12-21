import tkinter.messagebox
from tkinter import ttk
from tkinter import *
import datetime
from TeXport import *
from changedictlist import *

def func():
    print(0)

def notready():
    tkinter.messagebox.showinfo("Nicht fertig","Diese Funktion ist noch nicht fertiggestellt")

def makemenubar():
    mn = Menu(mainwin) 
    mainwin.config(menu=mn) 
    
    mn.add_command(label = "Öffnen", command=notready)
    mn.add_command(label = "Speichern", command=notready)
    mn.add_command(label="Exportieren", command=export)
    mn.add_command(label = 'Fahrt hinzufügen', command=lambda: addfahrt(terminedic, mainwin))

def export():
    texport(terminedic, 'preamble.tex', 'test.tex')
    makepdfanddisplay('test.tex')



def hline(inrow, width):
    for i in range(width):
        ttk.Separator(master=mainwin, orient=HORIZONTAL).grid(row=inrow, column=i,sticky="ew")

def savesettings(fahrtnr, fahrtwidget):
    sparte =1

    fahrtname = fahrtwidget.get()
    if not sparte: 
        tkinter.messagebox.showinfo("Wert fehlt","Der Wert Sparte fehlt")
        return 0
    elif not fahrtname: 
        tkinter.messagebox.showinfo("Wert fehlt","Der Wert Fahrtname fehlt")
        return 0
    
    terminedic[fahrtnr]['Fahrtname'] = fahrtname

    mainwin.update()
    printfahrten()
    
    

def editfahrt(fahrtnr):
    edit=Toplevel(mainwin)
    edit.title("Fahrt bearbeiten")
    edit.geometry('960x540')
    
    # 3 columns
    edit.columnconfigure(0, weight =2) # Description
    edit.columnconfigure(1, weight =1) # Enter Value/Select
    edit.columnconfigure(2, weight =1) # Only for calendar

    
    fahrt_name_desc = Label(edit, text="Fahrt Name:")
    fahrt_name_desc.grid(row=0, column=0,padx=5,pady=5,sticky=W)

    fahrt_name = terminedic[fahrtnr]['Fahrtname']
    fahrt_insert = Entry(edit, width=50, textvariable=fahrt_name)
    fahrt_insert.insert(0, terminedic[fahrtnr]['Fahrtname'])
    fahrt_insert.grid(row=0, column=1, padx=5,pady=5,sticky=E)
    
    save = Button(edit, text = "Speichern", command=lambda: savesettings(fahrtnr, fahrt_insert))
    save.grid(row=50,column=1)

    edit.mainloop()


def printfahrten(fahrtennr=None):

    for widget in mainwin.winfo_children(): # destroy all widgets
        widget.destroy()

    makemenubar()
    mainwin.columnconfigure(0, weight =1) # Startdatum
    mainwin.columnconfigure(1, weight =1) # Enddatum
    mainwin.columnconfigure(2, weight =2) # Sparte
    mainwin.columnconfigure(3, weight =4) # Name
    mainwin.columnconfigure(4, weight =1) # Pushbuttons

    startdatum_label = []
    enddatum_label = []
    sparte_label = []
    name_label = []
    edit_buttons =[]

    
    startdatum_label.append(Label(mainwin, text="Startdatum"))
    startdatum_label[0].grid(column=0,row=0,padx=5,pady=5, sticky=W)
    
    enddatum_label.append(Label(mainwin, text="Enddatum"))
    enddatum_label[0].grid(column=1,row=0,padx=5,pady=5, sticky=W)

    sparte_label.append(Label(mainwin, text="Sparte"))
    sparte_label[0].grid(column=2,row=0,padx=5,pady=5, sticky=W)

    name_label.append(Label(mainwin, text="Fahrtenname"))
    name_label[0].grid(column=3,row=0,padx=5,sticky=W)

    hline(1,5)


    if not fahrtennr:
        for increment in range(1,len(terminedic)+1):
            
            startdatum_label.append(Label(mainwin, text=daymonthyear(terminedic[increment-1]['StartDatum'])))
            startdatum_label[increment].grid(column=0,row=increment+1,padx=5,pady=5, sticky=W)

            enddatum_label.append(Label(mainwin, text=daymonthyear(terminedic[increment-1]['EndDatum'])))
            enddatum_label[increment].grid(column=1,row=increment+1,padx=5,pady=5, sticky=W)

            sparte_label.append(Label(mainwin, text=terminedic[increment-1]['Sparte']))
            sparte_label[increment].grid(column=2,row=increment+1,padx=5,pady=5, sticky=W)

            name_label.append(Label(mainwin, text=terminedic[increment-1]['Fahrtname']))
            name_label[increment].grid(column=3,row=increment+1,padx=5,pady=5, sticky=W)

            edit_buttons.append(Button(mainwin,text="Bearbeiten",command=lambda c=increment: editfahrt(c-1)))
            edit_buttons[increment-1].grid(column=4, row=increment+1,padx=5,pady=5,sticky=E)
    else:
        startdatum_label[fahrtennr+1].config(text=daymonthyear(terminedic[fahrtennr]['StartDatum']))
        enddatum_label[fahrtennr+1].config(text=daymonthyear(terminedic[fahrtennr]['EndDatum']))
        sparte_label[fahrtennr+1].config(text=terminedic[fahrtennr]['Sparte'])
        name_label[fahrtennr+1]["text"] = terminedic[fahrtennr]['Fahrtname']


#test
terminedic = []
# main





mainwin = tkinter.Tk(screenName=None, baseName=None, useTk=1) # Create mainwin
#Widgets here
mainwin.geometry('960x540')
mainwin.title("Fahrtenprogramm Generator")

printfahrten()
mainwin.mainloop()