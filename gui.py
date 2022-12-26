import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Scrollbar
import datetime
from TeXport import *
#from changedictlist import *
from basicgui import hline
from EditFahrten import EditFahrten

class MainWin(tk.Tk):
    
    __terminedic = [
        {
        'Sparte' : "Kanupolo",
        'Spartennr' : 0,
        'Fahrtname' : "Test",
        'Startzeit' : None,
        'Endzeit' : None,
        'StartDatum' : datetime.date(month=12,day=15,year=2023),
        'EndDatum' : None,
        'Ansprechpartner' : ["Leo", "mail", 'm', True], # 2D-Liste mit Ansprechpartner, Email. Wenn Länge>1: Ansprechpartner, Ansprechpartner KCW, Ansprechpartner n
        'AnsprechpartnerKCW' : None,
        'Fließtext' : None,
        'items' : [] # Liste mit Stichpunkten'
        },
        {
        'Sparte' : "Wildwasser",
        'Fahrtname' : "Salza",
        'Startzeit' : "09:00",
        'Endzeit' : "19:00",
        'StartDatum' : datetime.date(month=5,day=15,year=2023),
        'EndDatum' : datetime.date(month=5,day=19,year=2023),
        'Ansprechpartner' : ["bernd", "ww@verband.de", 'm', False], # 2D-Liste mit Ansprechpartner, Email. Wenn Länge>1: Ansprechpartner, Ansprechpartner KCW, Ansprechpartner n
        'AnsprechpartnerKCW' : ["Leo", "kcw@kcw.de", 'm', True],
        'Fließtext' : "asd",
        'items' : ["text", "text2"] # Liste mit Stichpunkten'
        }
    ]
    __sparten = ["Kanupolo", "Wildwasser"]
    __ansprechpartner = [["Leo", "kcw@kcw.de", 'm', True], ["bernd", "ww@verband.de", 'm', False]]


    def __init__(self):
        
        tk.Tk.__init__(self)
        self.minsize(900, 500)
        self.main_frame = tk.Frame(self)
        self.user_info_label = tk.Label(self)
        self.wm_title("Fahrtenbuch Generator")

        self.printfahrten()
        self.mainloop()

    def printfahrten(self, fahrtennr=None):


        frame = Scrollable(self)

       
        for widget in frame.winfo_children(): # destroy all widgets
            widget.destroy()

        self.__makemenubar()
        

        startdatum_label = []
        enddatum_label = []
        sparte_label = []
        name_label = []
        edit_buttons =[]

        frame.columnconfigure(0, weight =1) # Startdatum
        frame.columnconfigure(1, weight =1) # Enddatum
        frame.columnconfigure(2, weight =2) # Sparte
        frame.columnconfigure(3, weight =4) # Name
        frame.columnconfigure(4, weight =1) # Pushbuttons
        
        startdatum_label.append(tk.Label(frame, text="Startdatum"))
        startdatum_label[0].grid(column=0,row=0,padx=5,pady=5, sticky=tk.W)
        
        enddatum_label.append(tk.Label(frame, text="Enddatum"))
        enddatum_label[0].grid(column=1,row=0,padx=5,pady=5, sticky=tk.W)

        sparte_label.append(tk.Label(frame, text="Sparte"))
        sparte_label[0].grid(column=2,row=0,padx=5,pady=5, sticky=tk.W)

        name_label.append(tk.Label(frame, text="Fahrtenname"))
        name_label[0].grid(column=3,row=0,padx=5,sticky=tk.W)

        fahrt_add_btn = tk.Button(frame, text="Fahrt hinzufügen", command=lambda: self.__addfahrt(len(self.__terminedic)+1))
        fahrt_add_btn.grid(column=4,row=0,padx=5,sticky=tk.E)

        hline(frame, 1,5)


        if not fahrtennr:
            for increment in range(1,len(self.__terminedic)+1):
                
                startdatum_label.append(tk.Label(frame, text=daymonthyear(self.__terminedic[increment-1]['StartDatum'])))
                startdatum_label[increment].grid(column=0,row=increment+1,padx=5,pady=5, sticky=tk.W)

                enddatum_label.append(tk.Label(frame, text=daymonthyear(self.__terminedic[increment-1]['EndDatum'])))
                enddatum_label[increment].grid(column=1,row=increment+1,padx=5,pady=5, sticky=tk.W)

                sparte_label.append(tk.Label(frame, text=self.__terminedic[increment-1]['Sparte']))
                sparte_label[increment].grid(column=2,row=increment+1,padx=5,pady=5, sticky=tk.W)

                name_label.append(tk.Label(frame, text=self.__terminedic[increment-1]['Fahrtname']))
                name_label[increment].grid(column=3,row=increment+1,padx=5,pady=5, sticky=tk.W)

                edit_buttons.append(tk.Button(frame,text="Bearbeiten",command=lambda c=increment: self.__editfahrt(c-1)))
                edit_buttons[increment-1].grid(column=4, row=increment+1,padx=5,pady=5,sticky=tk.E)

        frame.update()

    def __editfahrt(self, number):
        EditFahrten(self, self.__sparten, self.__terminedic, self.__ansprechpartner, number)


    def __notready(self):

        msgbox.showinfo("Nicht fertig","Diese Funktion ist noch nicht fertiggestellt")

    def __makemenubar(self):

        mn = tk.Menu(self) 
        self.config(menu=mn) 
        
        mn.add_command(label = "Öffnen", command=self.__notready)
        mn.add_command(label = "Speichern", command=self.__notready)
        mn.add_command(label="Exportieren", command=self.__export)
        #mn.add_command(label = 'Fahrt hinzufügen', command=lambda: self.__addfahrt(len(self.__terminedic)+1))

    def __export(self):

        texport(self.__terminedic,self.__sparten, 'preamble.tex', 'test.tex')
        makepdfanddisplay('test.tex')

    def __addfahrt(self, number):

        EditFahrten(self, self.__sparten, self.__terminedic, self.__ansprechpartner, number)
        

class Scrollable(tk.Frame):
    """
       Make a frame scrollable with scrollbar on the right.
       After adding or removing widgets to the scrollable frame,
       call the update() method to refresh the scrollable area.
    """

    def __init__(self, frame, width=16):

        scrollbar = tk.Scrollbar(frame, width=width)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.canvas = tk.Canvas(frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=self.canvas.yview)

        self.canvas.bind('<Configure>', self.__fill_canvas)

        # base class initialization
        tk.Frame.__init__(self, frame)

        # assign this obj (the inner frame) to the windows item of the canvas
        self.windows_item = self.canvas.create_window(0,0, window=self, anchor=tk.NW)


    def __fill_canvas(self, event):
        "Enlarge the windows item to the canvas width"

        canvas_width = event.width
        self.canvas.itemconfig(self.windows_item, width = canvas_width)

    def update(self):
        "Update the canvas and the scrollregion"

        self.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox(self.windows_item))
    

#test

MainWin()