import tkinter.messagebox as msgbox
import tkinter as tk
import tkinter.ttk as ttk
from basicgui import *

class Ansprechpartner(Toplevel):

    __currentansprechpartner = []

    def __init__(self, mainwin, ansprechpartner):

        Toplevel.__init__(self, mainwin)
        self.title("Ansprechpartner bearbeiten")
        self.__currentansprechpartner = ansprechpartner
        self.makewindow()
        
        self.protocol("WM_DELETE_WINDOW", mainwin.makewindow)
        self.mainloop()

    def makewindow(self):

        self.minsize(350, 200)
        
        self.columnconfigure(0, weight =2) # Name
        self.columnconfigure(1, weight =2) # Mailadresse
        self.columnconfigure(2, weight =1) # Geschlecht
        self.columnconfigure(3, weight =1) # KCW Mitglied
        self.columnconfigure(4, weight =1) # Edit

        self.__printwidgets()

    def __printwidgets(self):

        for widget in self.winfo_children(): # destroy all widgets
            widget.destroy()

        name_label = []
        mail_label = []
        gender_label = []
        kcw_label = []
        edit = []

        name_label.append(Label(self, text="Name"))
        name_label[0].grid(column=0,row=0,padx=5,pady=5, sticky=W)

        mail_label.append(Label(self, text="Mail Adresse"))
        mail_label[0].grid(column=1,row=0,padx=5,pady=5, sticky=W)

        gender_label.append(Label(self, text="Geschlecht"))
        gender_label[0].grid(column=2,row=0,padx=5,pady=5, sticky=W)

        kcw_label.append((Label(self, text="KCW Mitglied")))
        kcw_label[0].grid(column=3,row=0,padx=5,pady=5, sticky=W)

        edit.append(Button(self, text='hinzufügen', command=self.__callAdd))
        edit[0].grid(column=4,row=0,padx=5,pady=5,sticky=E)

        hline(self, 1,4)

        for increment in range(len(self.__currentansprechpartner)):
            name_label.append(Label(self, text=self.__currentansprechpartner[increment][0]))
            name_label[increment+1].grid(column=0,row=increment+2,padx=5,pady=5, sticky=W)

            mail_label.append(Label(self, text=self.__currentansprechpartner[increment][1]))
            mail_label[increment+1].grid(column=1,row=increment+2,padx=5,pady=5, sticky=W)

            gender_label.append(Label(self, text=self.__currentansprechpartner[increment][2]))
            gender_label[increment+1].grid(column=2,row=increment+2,padx=5,pady=5, sticky=W)

            kcw_label.append((Label(self, text=str(self.__currentansprechpartner[increment][3]))))
            kcw_label[increment+1].grid(column=3,row=increment+2,padx=5,pady=5, sticky=W)

            edit.append(Button(self, text='löschen', command=lambda c=increment: self.__delete(c)))
            edit[increment+1].grid(column=4,row=increment+2,padx=5,pady=5,sticky=E)


    def __callAdd(self):
        AddSparte(self, self.__currentansprechpartner)

    def __delete(self, number):
        self.__currentansprechpartner.pop(number)
        self.__printwidgets()
        self.update()

class AddSparte(Toplevel):

    __currentansprech = []

    def __init__(self, mainwin, ansprech):

        Toplevel.__init__(self, mainwin)
        self.title("Ansprechpartner hinzufügen")
        self.__currentansprech = ansprech
        self.__makewindow()
        self.__mainwin = mainwin

        self.mainloop()

    def __makewindow(self):
        self.minsize(350, 200)
        
        self.columnconfigure(0, weight =1)
        self.columnconfigure(1, weight =1)

        self.__printwidgets()

    def __printwidgets(self):

        name_desc = Label(self, text="Name")
        name_desc.grid(row=0, column=0, padx=5,pady=5,sticky=W)

        name_entry = Entry(self, width=25)
        name_entry.grid(row=0, column=1, padx=5,pady=5,sticky=W)

        mail_desc = Label(self, text="Mail Adresse")
        mail_desc.grid(row=1, column=0, padx=5,pady=5,sticky=W)

        mail_entry = Entry(self, width=25)
        mail_entry.grid(row=1, column=1, padx=5,pady=5,sticky=W)

        gender_desc = Label(self, text="Geschlecht:")
        gender_desc.grid(row=2, column=0, padx=5,pady=5,sticky=W)

        gender = StringVar()
        genderlist = ["m", "w"]

        gender_entry = OptionMenu(self, gender, *genderlist)
        gender_entry.grid(row=2, column=1, padx=5,pady=5,sticky=W)

        kcw_label = Label(self, text = "KCW Mitglied:")
        kcw_label.grid(row=3, column=0, padx=5,pady=5,sticky=W)

        kcw_val = IntVar(value=0)
        kcw_select = Checkbutton(self,variable=kcw_val, text="Ja",onvalue=1,offvalue=0)
        kcw_select.grid(row=3, column=1, padx=5,pady=5,sticky=W)

        save_button = Button(self, text="Speichern", command=lambda: self.__save(name_entry.get(), mail_entry.get(), gender.get(), kcw_val.get()))
        save_button.grid(row=50,column=1, padx=5,pady=5,sticky=W)

    def __save(self, name, mail, gender, kcw):
        
        # check input
        if not name:
            msgbox.showwarning("Eingabe unvollständig", "Bitte Namen eingeben")
        elif not mail:
            msgbox.showwarning("Eingabe unvollständig", "Bitte Mailadresse eingeben")
        elif not gender:
            msgbox.showwarning("Eingabe unvollständig", "Bitte Geschlecht auswählen")
        else:
            # change list
            self.__currentansprech.append([name, mail, gender, bool(kcw)])
            self.__mainwin.makewindow()
            self.destroy()