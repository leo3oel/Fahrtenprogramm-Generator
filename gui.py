import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import Scrollbar
from tkinter import scrolledtext
import datetime
from TeXport import *
#from changedictlist import *
from basicgui import hline
from EditFahrten import EditFahrten
import os
from tkinter import filedialog
import json
from json import JSONEncoder
from dateutil import parser

class MainWin(tk.Tk):
    
    __file = None
    __filename = None
    __frame = None

    __terminedic = []
    __sparten = []
    __ansprechpartner = []

    __exportfilename= None
    __preamble_filename = None
    __vorbemerkung = ""

    def __init__(self):
        
        tk.Tk.__init__(self)
        self.minsize(900, 500)
        self.main_frame = tk.Frame(self)
        self.user_info_label = tk.Label(self)
        self.wm_title("Fahrtenbuch Generator")

        self.printfahrten()
        self.mainloop()

    def printfahrten(self, fahrtennr=None):

        if self.__frame:
            self.__frame.update()
        else:
            self.__frame = Scrollable(self)

        
        for widget in self.__frame.winfo_children(): # destroy all widgets
            widget.destroy()

        self.__makemenubar()
        

        startdatum_label = []
        enddatum_label = []
        sparte_label = []
        name_label = []
        edit_buttons =[]

        self.__frame.columnconfigure(0, weight =1) # Startdatum
        self.__frame.columnconfigure(1, weight =1) # Enddatum
        self.__frame.columnconfigure(2, weight =2) # Sparte
        self.__frame.columnconfigure(3, weight =4) # Name
        self.__frame.columnconfigure(4, weight =1) # Pushbuttons
        
        startdatum_label.append(tk.Label(self.__frame, text="Startdatum"))
        startdatum_label[0].grid(column=0,row=0,padx=5,pady=5, sticky=tk.W)
        
        enddatum_label.append(tk.Label(self.__frame, text="Enddatum"))
        enddatum_label[0].grid(column=1,row=0,padx=5,pady=5, sticky=tk.W)

        sparte_label.append(tk.Label(self.__frame, text="Sparte"))
        sparte_label[0].grid(column=2,row=0,padx=5,pady=5, sticky=tk.W)

        name_label.append(tk.Label(self.__frame, text="Fahrtenname"))
        name_label[0].grid(column=3,row=0,padx=5,sticky=tk.W)

        fahrt_add_btn = tk.Button(self.__frame, text="Fahrt hinzufügen", command=lambda: self.__addfahrt(len(self.__terminedic)+1))
        fahrt_add_btn.grid(column=4,row=0,padx=5,sticky=tk.E)

        hline(self.__frame, 1,5)

        if not fahrtennr:
            for increment in range(1,len(self.__terminedic)+1):
                
                startdatum_label.append(tk.Label(self.__frame, text=daymonthyear(self.__terminedic[increment-1]['StartDatum'])))
                startdatum_label[increment].grid(column=0,row=increment+2,padx=5,pady=5, sticky=tk.W)

                enddatum_label.append(tk.Label(self.__frame, text=daymonthyear(self.__terminedic[increment-1]['EndDatum'])))
                enddatum_label[increment].grid(column=1,row=increment+2,padx=5,pady=5, sticky=tk.W)

                sparte_label.append(tk.Label(self.__frame, text=self.__terminedic[increment-1]['Sparte']))
                sparte_label[increment].grid(column=2,row=increment+2,padx=5,pady=5, sticky=tk.W)

                name_label.append(tk.Label(self.__frame, text=self.__terminedic[increment-1]['Fahrtname']))
                name_label[increment].grid(column=3,row=increment+2,padx=5,pady=5, sticky=tk.W)

                edit_buttons.append(tk.Button(self.__frame,text="Bearbeiten",command=lambda c=increment: self.__editfahrt(c-1)))
                edit_buttons[increment-1].grid(column=4, row=increment+2,padx=5,pady=5,sticky=tk.E)

        self.__frame.update()

    def __makemenubar(self):

        mn = tk.Menu(self) 
        self.config(menu=mn) 
        
        mn.add_command(label = "Öffnen", command=self.__openfile)
        mn.add_command(label = "Speichern", command=self.__savefile)
        mn.add_command(label="Vorbemerkung bearbeiten", command=self.__vorbemerkungbearbeiten)
        mn.add_command(label="Exportieren", command=self.__exportwin)


    def __editfahrt(self, number):
        EditFahrten(self, self.__sparten, self.__terminedic, self.__ansprechpartner, number)


    def __openfile(self):
        
        if not self.__file:
            self.__file = filedialog.askopenfile()
            if self.__file:
                self.__filename = self.__file.name
                decoded = json.load(self.__file, object_hook=DecodeDateTime)
                self.__file.close()

                self.__terminedic = decoded[0]
                self.__ansprechpartner = decoded[1]
                self.__sparten = decoded[2]
                self.__vorbemerkung = decoded[3]

                self.printfahrten()


    def __savefile(self):
        
        if not self.__file:
            self.__file = filedialog.asksaveasfile(mode="w", initialfile=".fahrten")
            if self.__file:
                self.__filename = self.__file.name
                if self.__filename[-7:] != "fahrten":
                    msgbox.showerror("Ungültiger Dateiname", "Bitte Dateiname überprüfen")
                    os.remove(self.__filename)
                self.__file.write(self.__makejson())
                self.__file.close()
        else:
            with open(self.__filename, "w") as self.__file:
                self.__file.write(self.__makejson())


    def __makejson(self):
        
        return json.dumps([self.__terminedic, self.__ansprechpartner, self.__sparten, self.__vorbemerkung], cls=DateTimeEncoder, indent=4, ensure_ascii=False)
            

    def __exportwin(self):

        self.__exportwindow = tk.Toplevel(self)
        self.__exportwindow.title("Exportieren")

        self.__exportwindow.columnconfigure(0, weight =1)
        self.__exportwindow.columnconfigure(1, weight =1)

        dateiname_label = tk.Label(self.__exportwindow, text="Dateinamen:")
        dateiname_label.grid(column=0,row=0,padx=5,pady=5, sticky=tk.W)

        dateiname_button = tk.Button(self.__exportwindow, text="Ordner/Dateinamen auswaehlen", command=self.__selectexportfilename)
        dateiname_button.grid(column=1,row=0,padx=5,pady=5, sticky=tk.W)

        self.__tex = tk.IntVar()
        cb_tex = tk.Checkbutton(self.__exportwindow, text="LaTeX Datei", variable=self.__tex, onvalue=1,offvalue=0)
        cb_tex.grid(column=0,row=2, columnspan=2,padx=5,pady=5)
        self.__tex.trace("w", self.__togglepreamble)

        pdf = tk.IntVar()
        self.__cb_pdf = tk.Checkbutton(self.__exportwindow, text="PDF Dokument, benötigt LaTeX Installation", variable=pdf, onvalue=1,offvalue=0)
        self.__cb_pdf.grid(column=0,row=3, columnspan=2,padx=5,pady=5)
        self.__cb_pdf.grid_remove()

        self.__preamble_label = tk.Label(self.__exportwindow, text="Preamble:")
        self.__preamble_label.grid(column=0,row=4,padx=5,pady=5, sticky=tk.W)
        self.__preamble_label.grid_remove()

        keeplogs = tk.IntVar()
        self.__keeplogs = tk.Checkbutton(self.__exportwindow, text="Log Dateien behalten", variable=keeplogs, onvalue=1,offvalue=0)
        self.__keeplogs.grid(column=0,row=4, columnspan=2,padx=5,pady=5)
        self.__keeplogs.grid_remove()

        self.__preamble_button = tk.Button(self.__exportwindow, text="Preamble öffnen", command=self.__openpreamble)
        self.__preamble_button.grid(column=1,row=5,padx=5,pady=5, sticky=tk.W)
        self.__preamble_button.grid_remove()

        export_btn = tk.Button(self.__exportwindow, text="Exportieren", command=lambda: self.__export(self.__tex.get(),pdf.get(), keeplogs.get()))
        export_btn.grid(column=0,row=50, columnspan=2,padx=5,pady=5)

        self.__exportwindow.mainloop()


    def __vorbemerkungbearbeiten(self):

        vorbemerkungswindow = tk.Toplevel(self)
        vorbemerkungswindow.title("Vorbemerkung bearbeiten")

        vorbemerkungswindow.columnconfigure(0, weight=1)

        text_label = tk.Label(vorbemerkungswindow, text="Bitte Text eingeben, LaTeX Commands werden unterstützt:")
        text_label.grid(column=0,row=0,padx=5,pady=5, sticky=tk.W)

        text_entry = scrolledtext.ScrolledText(vorbemerkungswindow, wrap=tk.WORD, width=200, height=40)
        text_entry.grid(column=0,row=1,padx=5,pady=5, sticky=tk.W)
        
        text_entry.insert(tk.END, self.__vorbemerkung)

        save_bt = tk.Button(vorbemerkungswindow, text="Speichern", command=lambda: self.__savevorbemerkung(text_entry.get("1.0", tk.END), vorbemerkungswindow))
        save_bt.grid(column=0,row=2)

        vorbemerkungswindow.mainloop()

    
    def __savevorbemerkung(self, text, topwin):
        
        # delete linebreaks
        if text:
            char = text[-1]
            while char == "\n":
                text = text[:-1]
                char = text[-1]
        self.__vorbemerkung = text
        topwin.destroy()

    def __togglepreamble(self, *args):

        if self.__tex.get():
            self.__preamble_label.grid()
            self.__preamble_button.grid()
            self.__cb_pdf.grid()
            self.__keeplogs.grid()
        else:
            self.__preamble_label.grid_remove()
            self.__preamble_button.grid_remove()
            self.__cb_pdf.grid_remove()
            self.__keeplogs.grid_remove()

    
    def __openpreamble(self):

        preamble = filedialog.askopenfile(parent=self.__exportwindow)
        if preamble:            
            self.__preamble_filename = preamble.name
            preamble.close


    def __selectexportfilename(self):
        
        msgbox.showinfo("Bitte keine Dateiendung eingeben", "Bitte keine Dateiendung eingeben, Dateiendungen werden automatisch festgelegt", parent=self.__exportwindow)
        efile = filedialog.asksaveasfile(parent=self.__exportwindow)
        if efile:
            self.__exportfilename = efile.name
            efile.close()
            os.remove(self.__exportfilename)


    def __export(self, tex, pdf, logs):

        if not self.__exportfilename:
            msgbox.showerror("Fehler", "Bitte Zieldatei auswählen")
            return 0

        texfilename = self.__exportfilename+".tex"
        if tex:
            if not self.__preamble_filename:
                msgbox.showerror("Fehler", "Bitte Preamble auswählen")
                return 0 
            else:
                texport(self.__terminedic,self.__sparten, self.__preamble_filename, texfilename, self.__ansprechpartner, self.__vorbemerkung)
        if pdf:
            makepdfanddisplay(texfilename)
        if logs:
            pass
        else:
            os.remove(self.__exportfilename+".toc")
            os.remove(self.__exportfilename+".out")
            os.remove(self.__exportfilename+".aux")
            os.remove(self.__exportfilename+".log")

        self.__exportwindow.destroy()


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
    
class DateTimeEncoder(JSONEncoder):
        #Override the default method
        def default(self, obj):
            if isinstance(obj, (datetime.date, datetime.datetime)):
                return obj.isoformat()
#test

def DecodeDateTime(empDict):
    if 'StartDatum' in empDict:
        empDict["StartDatum"] = parser.parse(empDict["StartDatum"]).date()
    if 'EndDatum' in empDict:
        if empDict["EndDatum"]:
            empDict["EndDatum"] = parser.parse(empDict["EndDatum"]).date()
    return empDict


MainWin()