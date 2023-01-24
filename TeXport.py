import datetime
import shutil
import subprocess
from DateTime import daymonth
from icalendar import Calendar, Event, vCalAddress, vText
import pytz
import os
from os.path import exists


def makepdfanddisplay(filename, logs):
    cwd = os.getcwd()
    path = os.path.dirname(filename)
    os.chdir(path)
    for i in range(3):
        subprocess.run(["lualatex", filename])
    if not logs:
        deleteLatexLogs(filename)
    subprocess.Popen(["zathura", filename[:-3]+"pdf"])
    os.chdir(cwd)


def deleteLatexLogs(filename):
    exportfilename = filename[:-4]
    if exists(exportfilename + ".toc"):
        os.remove(exportfilename + ".toc")
    if exists(exportfilename + ".out"):
        os.remove(exportfilename + ".out")
    if exists(exportfilename + ".aux"):
        os.remove(exportfilename + ".aux")
    if exists(exportfilename + ".log"):
        os.remove(exportfilename + ".log")


def structurizelist(terminList):

    # Sort List by Date
    terminList = sorted(terminList, key=lambda i: i['StartDatum'])
    return terminList

# TODO: Break down in smaller parts
def texport(terminefilename, spartenlisteold, preamble, filenameOut, ansprechpartnerliste, bemerkungenvorneweg=None):
    '''
    Exports a list of dictionarys into a tex file, needs to import a preamble
    '''
    spartenliste = []
    terminefilename = structurizelist(terminefilename)
    # check for needed sparten
    for sparte in spartenlisteold:
        for fahrt in terminefilename:
            if (sparte == fahrt['Sparte']):
                if fahrt['Sparte'] in spartenliste:
                    pass
                else:
                    spartenliste.append(sparte)

    # Copy Logo
    shutil.copyfile(os.path.join(os.path.dirname(preamble), "logo.png"), os.path.join(os.path.dirname(filenameOut), "logo.png"))

    # Read in Preamble
    with open(preamble) as inpreamble:
        preamble = inpreamble.read()

    # Mark hyperlinks APPEND DICTIONARY
    for fahrt in terminefilename:
        list = []
        for item in range(len(fahrt['items'])):
            list.append(markhyperlinks(fahrt['items'][item]))
        dict1 = {'PrintFliesstext': markhyperlinks(fahrt['Fliesstext']), 'Printitems': list}
        fahrt.update(dict1)

    clearfliesstext(terminefilename)

    # Print out TeX
    with open(filenameOut, 'w') as texfile:

        # Write Preamble
        texfile.write(preamble + "\n\n%%%%%%%%%%%%%%%%%%%%% Generated File %%%%%%%%%%%%%%%%%%%%%\n")
        for sparte in spartenliste:
            texfile.write("\\fancypagestyle{" + sparte + "}{\n"
                + "    \\fancyhead[L]{\\Large{\\textsc{" + sparte + "}}}\n"
                + "    \\fancyhead[R]{\\includegraphics[width=1.75cm]{logo.png}}\n"
                + "    \\renewcommand{\\headrulewidth}{0.5pt}\n"
                + "    \\cfoot{\\thepage}\n"
                + "}\n\n"
            )

        texfile.write("\\begin{document}\n\n"
            + "\\begingroup" + "\n"
            + "    \\hypersetup{hidelinks}" + "\n"
            + "    \\tableofcontents\\thispagestyle{fancy}" + "\n"
            + "\\endgroup" + "\n"
            + "\\reversemarginpar" + "\n" + "\n"
        )

        if bemerkungenvorneweg:
            bemerkungenvorneweg = markhyperlinks(bemerkungenvorneweg)
            texfile.write("\\section*{Bemerkungen}")
            texfile.write(bemerkungenvorneweg)


        for sparte in spartenliste:
            texfile.write("\\chapter*{")
            texfile.write(sparte + "}\n")
            texfile.write("\\thispagestyle{" + sparte + "}\n" +
                          "\\addcontentsline{toc}{chapter}{\\protect\\numberline{}" + sparte + "}\n")
            texfile.write("\\pagestyle{" + sparte + "}\n")

            monat = -1
            monatsnamen = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                           "August", "September", "Oktober", "November", "Dezember"]

            for Fahrt in terminefilename:

                if Fahrt['Sparte'] == sparte:

                    if (Fahrt['StartDatum'].month-1) != monat:
                        monat = (Fahrt['StartDatum'].month-1)
                        if monat < len(monatsnamen):
                            texfile.write("\\section*{" + monatsnamen[monat] + "}")

                    # Print Paragraphname
                    texfile.write("\\paragraph{"+Fahrt['Fahrtname']+"}")

                    # Print Marginnote
                    texfile.write("\\marginnote{")
                    if Fahrt["EndDatum"]:
                        texfile.write(daymonth(Fahrt['StartDatum']) + " - " + daymonth(Fahrt["EndDatum"]))
                        if Fahrt["Startzeit"] and Fahrt["Endzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write(Fahrt['Startzeit'] + " - " + Fahrt['Endzeit'])
                        elif Fahrt["Startzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write("ab " + Fahrt['Startzeit'])
                    else:
                        texfile.write(daymonth(Fahrt['StartDatum']))
                        if Fahrt["Startzeit"] and Fahrt["Endzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write(Fahrt['Startzeit']+ " - " +  Fahrt['Endzeit'])
                        elif Fahrt["Startzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write("ab " + Fahrt['Startzeit'])
                    texfile.write("}\n")

                    # Print Fliesstext
                    if(Fahrt['PrintFliesstext']):
                        texfile.write("\\mbox{}\\\\\\mbox{}"+Fahrt['Fliesstext'])

                    # Print items
                    texfile.write("\\begin{itemize}\n")
                    ansprechpartner = []
                    ansprechpartnerkcw = []
                    for item in ansprechpartnerliste:
                        if Fahrt['Ansprechpartner'] in item:
                            ansprechpartner = item
                    if Fahrt['AnsprechpartnerKCW']:
                        for item in ansprechpartnerliste:
                            if Fahrt['AnsprechpartnerKCW'] in item:
                                ansprechpartnerkcw = item

                    if ansprechpartner:
                        if ansprechpartner[2] == 'w':
                            texfile.write("    \\item Ansprechpartnerin: ")
                        else:
                            texfile.write("    \\item Ansprechpartner: ")
                        texfile.write(ansprechpartner[0] + " \\href{"+ "mailto:"  +ansprechpartner[1] +
                                      "}{"+ ansprechpartner[1] + "}\n")
                        if(Fahrt['AnsprechpartnerKCW']):
                            if ansprechpartnerkcw:
                                if ansprechpartnerkcw[2] == 'w':
                                    texfile.write("    \\item Ansprechpartnerin KCW: ")
                                else:
                                    texfile.write("    \\item Ansprechpartner KCW: ")
                                texfile.write(ansprechpartnerkcw[0] + " \\href{"+ "mailto:"  +ansprechpartnerkcw[1] +
                                              "}{"+ ansprechpartnerkcw[1] + "}\n")
                            else:
                                texfile.write("\\item {\\color{red} Ansprechpartner " + Fahrt['AnsprechpartnerKCW'] +
                                              " konnte nicht gefunden werden. Bitte Ansprechpartner liste überprüfen}")
                    else:
                        texfile.write("\\item {\\color{red} Ansprechpartner " + Fahrt['Ansprechpartner'] +
                                      " konnte nicht gefunden werden. Bitte Ansprechpartner liste überprüfen}")

                    if Fahrt['Printitems']:
                        for item in Fahrt['Printitems']:
                            texfile.write("    \\item " + item + "\n")
                    texfile.write("\\end{itemize}\n\n")
            texfile.write("\n")
        texfile.write("\\end{document}")

    for fahrt in terminefilename:
        fahrt.pop("Printitems")
        fahrt.pop('PrintFliesstext')


def markhyperlinks(string):

    outputstring = ""
    currentword = ""
    for char in string:
        if char == " " or char == "\n" or char == "," or char == ";":
            if currentword[0:4] =="www.":
                currentword = "\\href{" + currentword + "}{"+currentword+"}"
            outputstring += currentword + char
            currentword = ""
        else:
            currentword += char
    if currentword[0:4] =="www.":
        currentword = "\\url{" + currentword + "}"
    outputstring += currentword
    return outputstring

def clearfliesstext(dict):
    """
    Deltes \n at the end
    """

    for dic in dict:
        string = dic['Fliesstext']
        if string:
            char = string[-1]
            while char == "\n":
                string = string[:-1]
                char = string[-1]
            dic['Fliesstext'] = string

class ICSexport():

    def __init__(self, terminefilename, ansprechpartnerliste):
        self.termineliste = terminefilename
        self.ansprechpartner = ansprechpartnerliste
        self.icsfile = Calendar()
        self.icsfile.add('prodid', '-//Paddel Kalender//')
        self.icsfile.add('version', '2.0')

    def export(self, filename):
        if not self.termineliste:
            return 0
        structurizelist(self.termineliste)
        for fahrtindex in range(len(self.termineliste)):
            self.makecsvdate(fahrtindex)
        with open(filename, "wb") as file:
            file.write(self.icsfile.to_ical())

    def makecsvdate(self, number):
        event = Event()
        event.add('name', self.termineliste[number]['Fahrtname'])
        event.add('description', self.getdescription(number))
        event.add('dtstart', self.getdate("Start",number))
        event.add('dtend', self.getdate("End",number))
        self.icsfile.add_component(event)

    def getdescription(self, number):
        description = ''
        for item in self.termineliste[number]['items']:
            description += item + "\n"

    def getansprechpartnerasstring(self, number):
        # Get Ansprechpartner index
        # -> Gender correctly
        # -> print name + mail
        # -> same for non KCW Ansprechpartner
        pass

    def getdate(self, type,number):
        """
        If startzeit but no endzeit just assume 4 hours
        Names not working
        """

        date = self.termineliste[number][f'{type}Datum']
        zeit = self.termineliste[number][f'{type}zeit']

        if zeit and not date:
            date = self.termineliste[number][f'StartDatum']
            date =  datetime.datetime(date.year, date.month, date.day, zeit.hour, zeit.minute, 0)#, tzinfo=pytz.utc)
            return date
        elif zeit:
            date =  datetime.datetime(date.year, date.month, date.day, zeit.hour, zeit.minute, 0)#, tzinfo=pytz.utc)
            return date
        elif date:
            return datetime.datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=pytz.utc)
        else:
            date = self.termineliste[number][f'StartDatum']
            date += datetime.timedelta(days=1)
            return datetime.datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=pytz.utc)