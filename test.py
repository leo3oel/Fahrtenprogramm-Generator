from EditFahrten import appenddictionarylist
import datetime
import tkinter as tk
from tkinter import ttk

class Mainwin(tk.Tk):
    
    def __init__(self):
        tk.Tk.__init__(self)
        self.minsize(350, 200)
        self.main_frame = tk.Frame(self)
        self.user_info_label = tk.Label(self)
        self.wm_title("Test")

# Define Basics
def testsettings():
    terminedic = []
    # Name, Mail, geschlecht, KCW?
    ansprechpartner = [
        ['Leo', 'sport@kc-wuerzburg.de', 'm', True],
        ['Sebastian', 'wildwasser@kc-wuerzburg.de', 'm', True],
        ['Julia', 'jugend@kc-wuerzburg.de', 'w', True],
        ['Bernd Sachs', 'wildwasser@kanu-bayern.de', 'm', False]
    ]
    

    # Append Terminelist
    appenddictionarylist(
        liste = terminedic,
        inSparte = 'Allgemein',
        inFahrtname = "Arbeitsdienst",
        inSpartennr = 0,
        inStartDatum = datetime.date(2023,1,1),
        inAnsprechpartner = ansprechpartner[0],
        inStartzeit= datetime.time(9,0),
        inItems = ["Beispiel 1", "Text"]
    )
    appenddictionarylist(
        liste = terminedic,
        inSparte = 'Jugend',
        inFahrtname = "irgendwas für die jugend",
        inSpartennr = 1,
        inStartDatum = datetime.date(2023,1,3),
        inEndDatum = datetime.date(2023,1,5),
        inAnsprechpartner = ansprechpartner[2],
        inItems = ["Beispiel 2", "Text"]
    )
    appenddictionarylist(
        liste = terminedic,
        inSparte = 'Kanupolo',
        inFahrtname = "Boote flicken",
        inSpartennr = 3,
        inStartDatum =  datetime.date(2023,4,6),
        inStartzeit= datetime.time(12,0),
        inEndzeit= datetime.time(15,0),
        inAnsprechpartner = ansprechpartner[0],
        inItems = ["Boote flicken"]
    )
    appenddictionarylist(
        liste = terminedic,
        inSparte = 'Jugend',
        inFahrtname = "irgendwas für die jugend",
        inSpartennr = 1,
        inStartDatum = datetime.date(2023,6,7),
        inEndDatum = datetime.date(2023,6,9),
        inAnsprechpartner = ansprechpartner[2],
        inItems = ["Beispiel 2", "Text"]
    )
    appenddictionarylist(
        liste = terminedic,
        inSparte = 'Wildwasser',
        inFahrtname = "Lehrgang Christi Himmelfahrt",
        inSpartennr = 2,
        inStartDatum = datetime.date(2023,5,18),
        inEndDatum = datetime.date(2023,5,21),
        inAnsprechpartner = ansprechpartner[3],
        inAnsprechpartnerKCW = ansprechpartner[2],
        inFließtext = "n bissi text",
        inItems = ["Paddeln auf der Salza", "Bissi Bootfahren"]
    )
    sparten = ["Allgemein", "Polo", "Wildwasser"]
    return ansprechpartner, terminedic, sparten