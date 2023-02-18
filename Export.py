import datetime
import shutil
import subprocess
from DateTime import daymonth
from icalendar import Calendar, Event, vCalAddress, vText
import pytz
import os
from os.path import exists

class Export:

    def __init__(self, termineDict, spartenList, personsList, filename, bemerkungen=None):
        self._termineDict = self.structurizeList(termineDict)
        self._spartenListe = self.getNeededSparten(spartenList, termineDict)
        self._personsListe = personsList
        self._filename = filename
        self._bemerkungen = bemerkungen
        self._monatsnamen = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
                             "August", "September", "Oktober", "November", "Dezember"]

    @staticmethod
    def structurizeList(termineDict):
        # Sort List by Date
        sortedTermineDict = sorted(termineDict, key=lambda i: i['StartDatum'])
        return sortedTermineDict

    def _clearFliesstext(self, dict):
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

    def getNeededSparten(self, spartenListe, termineDict):
        neededSpartenListe = []
        for sparte in spartenListe:
            for termin in termineDict:
                if (sparte == termin['Sparte']) and termin['Sparte'] not in neededSpartenListe:
                    neededSpartenListe.append(sparte)
        return neededSpartenListe

    def tab(self, n=1):
        out = ""
        for i in range(n):
            out += "    "
        return out

class ExportTex(Export):

    def __init__(self, termineDict, spartenList, personsList, filename, preamble, bemerkungen=None):
        super().__init__(termineDict, spartenList, personsList, filename, bemerkungen)
        self._preamble = preamble
        self.__printedFahrten = []

    def generateTex(self, withChapter, withOutChapter):
        self.__copyLogo(self._preamble, self._filename)
        self.__readPreamble()
        self.__searchForHyperlinks()
        self._clearFliesstext(self._termineDict)
        if withChapter:
            self.__writeTex()
        if withOutChapter:
            self.__writeTexWithOutChapter()
        self.__clearDict()

    def __copyLogo(self, preamble, filename):
        shutil.copyfile(os.path.join(os.path.dirname(preamble), "logo.png"),
                        os.path.join(os.path.dirname(filename), "logo.png"))

    def __searchForHyperlinks(self):
        for termin in self._termineDict:
            items = []
            for item in range(len(termin['items'])):
                items.append(self.__markHyperlinks(termin['items'][item]))
            fliessText = self.__markHyperlinks(termin['Fliesstext'])
            tempDict = {'PrintFliesstext': fliessText, 'Printitems': items}
            termin.update(tempDict)

    def __markHyperlinks(self, string):
        outputString = ""
        currentWord = ""
        for char in string:
            if char == " " or char == "\n" or char == "," or char == ";":
                if currentWord[0:4] == "www.":
                    currentWord = "\\href{" + currentWord + "}{" + currentWord + "}"
                outputString += currentWord + char
                currentWord = ""
            else:
                currentWord += char
        if currentWord[0:4] == "www.":
            currentWord = "\\url{" + currentWord + "}"
        outputString += currentWord
        return outputString

    def __writeTex(self):
        output = self.__readPreamble()
        output += self.__generateFancyHead()
        output += self.__generateDocumentStart()
        output += self.__generateBemerkungen()
        output += self.__generateChapters()
        output += self.__generateClosing()
        filename = self._filename + ".tex"
        self.__writeToFile(output, filename)

    def __writeTexWithOutChapter(self):
        output = self.__readPreamble()
        output += self.__generateDocumentStartWithoutChapter()
        output += self.__generateBemerkungen()
        output += "\\pagebreak[4]\n"
        output += self.__generateTermine()
        output += self.__generateClosing()
        filename = self._filename + "-nochapter.tex"
        self.__writeToFile(output, filename)

    def __readPreamble(self):
        with open(self._preamble) as preamble:
            preamble = preamble.read()
        return preamble

    def __generateFancyHead(self):
        out = "\n\n%%%%%%%%%%%%%%%%%%%%% Generated File %%%%%%%%%%%%%%%%%%%%%\n"
        for sparte in self._spartenListe:
            out += "\\fancypagestyle{" + sparte + "}{\n"
            out += "    \\fancyhead[L]{\\Large{\\textsc{" + sparte + "}}}\n"
            out += "    \\fancyhead[R]{\\includegraphics[width=1.75cm]{logo.png}}\n"
            out += "    \\renewcommand{\\headrulewidth}{0.5pt}\n"
            out += "    \\cfoot{\\thepage}\n"
            out += "}\n\n"
        return out

    def __generateDocumentStartWithoutChapter(self):
        out = "\n\n%%%%%%%%%%%%%%%%%%%%% Generated File %%%%%%%%%%%%%%%%%%%%%\n"
        out += "\\fancypagestyle{" + "Fahrtenprogramm" + "}{\n"
        out += "    \\fancyhead[L]{\\Large{\\textsc{" + "Fahrtenprogramm" + "}}}\n"
        out += "    \\fancyhead[R]{\\includegraphics[width=1.75cm]{logo.png}}\n"
        out += "    \\renewcommand{\\headrulewidth}{0.5pt}\n"
        out += "    \\cfoot{\\thepage}\n"
        out += "}\n\n"
        out += "\\begin{document}\n\n"
        out += "\\reversemarginpar" + "\n" + "\n"
        return out

    def __generateDocumentStart(self, toc = True):
        out = "\\begin{document}\n\n"
        if toc:
            out += "\\begingroup" + "\n"
            out += "    \\hypersetup{hidelinks}" + "\n"
            out += "    \\tableofcontents\\thispagestyle{fancy}" + "\n"
            out += "\\endgroup" + "\n"
        out += "\\reversemarginpar" + "\n" + "\n"
        return out

    def __generateBemerkungen(self):
        if self._bemerkungen:
            bemerkungen = self.__markHyperlinks(self._bemerkungen)
            out = "\\section*{Bemerkungen}"
            out += bemerkungen
            return out

    def __generateChapters(self):
        out = ""
        for sparte in self._spartenListe:
            out += "\\chapter*{"
            out += sparte + "}\n"
            out += "\\thispagestyle{" + sparte + "}\n"
            out += "\\addcontentsline{toc}{chapter}{\\protect\\numberline{}" + sparte + "}\n"
            out += "\\pagestyle{" + sparte + "}\n"
            out += self.__generateTermine(sparte)
        return out

    def __generateTermine(self, sparte = None):
        self.__monat = -1
        monatsnamen = self._monatsnamen
        out = ""
        for termin in self._termineDict:
            if sparte:
                if termin['Sparte'] == sparte:
                    out += self.__generateSection(termin, monatsnamen)
                    out += self.__generateSingleTermin(termin)
            elif [termin["Fahrtname"], termin['StartDatum']] not in self.__printedFahrten:
                sparten = self.__checkForOtherSparten(termin['Fahrtname'])
                self.__printedFahrten.append([termin['Fahrtname'], termin['StartDatum']])
                out += self.__generateSection(termin, monatsnamen)
                out += self.__generateSingleTermin(termin, sparten)

        return out

    def __checkForOtherSparten(self, terminName):
        spartenListe = []
        for termin in self._termineDict:
            if (termin['Fahrtname'] == terminName) and (termin['Sparte'] not in spartenListe):
                spartenListe.append(termin['Sparte'])
        return ", ".join(spartenListe)


    def __generateSingleTermin(self, termin, sparten=None):
        out = ""
        out += self.__generateParagraphAndMargin(termin, sparten)
        out += self.__generateFliesstextAndItems(termin)
        return out

    def __generateSection(self, termin, monatsnamen):
        out = ""
        if (termin['StartDatum'].month - 1) != self.__monat:
            self.__monat = (termin['StartDatum'].month - 1)
            if self.__monat < len(monatsnamen):
                out += ("\\section*{" + monatsnamen[self.__monat] + "}")
        return out
    def __generateParagraphAndMargin(self, termin, sparten):
        # Print Paragraphname
        out = "\\paragraph{" + termin['Fahrtname'] + "}"

        # Print Marginnote
        out += "\\marginnote{"
        if sparten:
            out += sparten + "\\\\"
        if termin["EndDatum"]:
            out += daymonth(termin['StartDatum']) + " - " + daymonth(termin["EndDatum"])
            if termin["Startzeit"] and termin["Endzeit"]:
                out += " \\\\ "
                out += termin['Startzeit'] + " - " + termin['Endzeit']
            elif termin["Startzeit"]:
                out += " \\\\ "
                out += "ab " + termin['Startzeit']
        else:
            out += daymonth(termin['StartDatum'])
            if termin["Startzeit"] and termin["Endzeit"]:
                out += " \\\\ "
                out += termin['Startzeit'] + " - " + termin['Endzeit']
            elif termin["Startzeit"]:
                out += " \\\\ "
                out += "ab " + termin['Startzeit']
        out += "}\n"
        return out

    def __generateFliesstextAndItems(self, termin):
        out = ""
        # Print Fliesstext
        if (termin['PrintFliesstext']):
            out += "\\mbox{}\\\\\\mbox{}" + termin['Fliesstext']

        # Print items
        out += "\\begin{itemize}\n"
        ansprechpartner = []
        ansprechpartnerkcw = []
        for item in self._personsListe:
            if termin['Ansprechpartner'] in item:
                ansprechpartner = item
        if 'AnsprechpartnerKCW' in termin:
            for item in self._personsListe:
                if termin['AnsprechpartnerKCW'] in item:
                    ansprechpartnerkcw = item

        if ansprechpartner:
            if ansprechpartner[2] == 'w':
                out += "    \\item Ansprechpartnerin: "
            else:
                out += "    \\item Ansprechpartner: "
            out += ansprechpartner[0] + " \\href{" + "mailto:" + ansprechpartner[1]
            out += "}{" + ansprechpartner[1] + "}\n"
            if termin['AnsprechpartnerKCW']:
                if ansprechpartnerkcw:
                    if ansprechpartnerkcw[2] == 'w':
                        out += "    \\item Ansprechpartnerin KCW: "
                    else:
                        out += "    \\item Ansprechpartner KCW: "
                    out += ansprechpartnerkcw[0] + " \\href{" + "mailto:" + ansprechpartnerkcw[1]
                    out += "}{" + ansprechpartnerkcw[1] + "}\n"
                else:
                    out += "\\item {\\color{red} Ansprechpartner " + termin['AnsprechpartnerKCW']
                    out += " konnte nicht gefunden werden. Bitte Ansprechpartner liste überprüfen}"
        else:
            out += "\\item {\\color{red} Ansprechpartner " + termin['Ansprechpartner']
            out += " konnte nicht gefunden werden. Bitte Ansprechpartner liste überprüfen}"
        if termin['Printitems']:
            for item in termin['Printitems']:
                out += "    \\item " + item + "\n"
        out += "\\end{itemize}\n\n"
        return out

    def __generateClosing(self):
        out = "\n\\end{document}"
        return out

    def __clearDict(self):
        for termin in self._termineDict:
            if "Printitems" in termin:
                termin.pop("Printitems")
            if "PrintFliesstext" in termin:
                termin.pop("PrintFliesstext")

    def generatePdfs(self, logs, display, withchapters, withoutchapters):
        if withchapters:
            filename = self._filename + ".tex"
            self.__makePdf(logs, display, filename)
        if withoutchapters:
            filename = self._filename + "-nochapter.tex"
            self.__makePdf(logs, display, filename)

    def __makePdf(self, logs, display, filename):
        cwd = os.getcwd()
        path = os.path.dirname(filename)
        os.chdir(path)
        for i in range(3):
            subprocess.run(["lualatex", filename])
        if not logs:
            self.__deleteLatexLogs(filename)
        if display:
            subprocess.Popen(["zathura", filename[:-3] + "pdf"])
        os.chdir(cwd)

    def __deleteLatexLogs(self, filename):
        exportfilename = filename[:-4]
        if exists(exportfilename + ".toc"):
            os.remove(exportfilename + ".toc")
        if exists(exportfilename + ".out"):
            os.remove(exportfilename + ".out")
        if exists(exportfilename + ".aux"):
            os.remove(exportfilename + ".aux")
        if exists(exportfilename + ".log"):
            os.remove(exportfilename + ".log")

    def __writeToFile(self, string, filename):
        with open(filename, 'w') as file:
            file.write(string)


class ExportHTML(Export):
    def __init__(self, termineDict, spartenList, personsList, filename, bemerkungen=None):
        super().__init__(termineDict, spartenList, personsList, filename, bemerkungen)
        self._monat = 0

    def _getSurrounding(self, tag, text):
        return f"<{tag}>" + text + f"</{tag}>"

    def _formatDict(self):
        for termin in self._termineDict:
            items = []
            for item in range(len(termin['items'])):
                items.append(self._formatLinks(termin['items'][item]))
            fliessText = self._formatLinks(termin['Fliesstext'])
            tempDict = {'PrintFliesstext': fliessText, 'Printitems': items}
            termin.update(tempDict)

    def _formatLinks(self, string):
        words = string.split()
        for index, word in enumerate(words):
            if word.startswith("www."):
                words[index] = f'<a href="{word}">{word}</a>'
        return " ".join(words)

    def _clearDict(self):
        for termin in self._termineDict:
            if "Printitems" in termin:
                termin.pop("Printitems")
            if "PrintFliesstext" in termin:
                termin.pop("PrintFliesstext")

    def generateHTML(self):
        self._formatDict()
        head = self._generateHead()
        spartenOutput = self._generateSpartenOutput(self._spartenListe)
        foot = "\n</body>\n</html>"
        self._writeToFiles(self._spartenListe, head, spartenOutput, foot)
        self._clearDict()

    def _generateHead(self):
        out = "<!DOCTYPE html>\n" + "\n"
        out += "<!-- Auto Generated by Fahrtenprogramm Generator -->\n"
        out += "<html>" + "\n"
        out += "<head>" + "\n"
        out += self.tab() + "<style>" + "\n"
        out += self.tab(2) + "th, td {" + "\n"
        out += self.tab(2) + "padding-right: 20px;" + "\n"
        out += self.tab(2) + "}" + "\n"
        out += self.tab(2) + "ul{" + "\n"
        out += self.tab(3) + "padding-left: 0;" + "\n"
        out += self.tab(2) + "}" + "\n"
        out += self.tab() + "</style>" + "\n"
        out += "</head>" + "\n" + "\n"
        out += "<body>" + "\n"
        return out

    def _generateSpartenOutput(self, spartenListe):
        outputList = []
        for sparte in spartenListe:
            out = f"<h2>{sparte}</h2>\n"
            out += self._generateTermine(sparte)
            outputList.append(out)
        return outputList

    def _generateTermine(self, sparte):
        out = ""
        for termin in self._termineDict:
            if termin["Sparte"] == sparte:
                out += self._generateMonth(termin)
                out += self._generateSingleTermin(termin)
        return out

    def _generateMonth(self, termin):
        out = ""
        if (termin['StartDatum'].month - 1) != self._monat:
            self._monat = (termin['StartDatum'].month - 1)
            if self._monat < len(self._monatsnamen):
                out = f"<h3>{self._monatsnamen[self._monat]}</h3>\n"
        return out

    def _generateSingleTermin(self, termin):
        out = ""
        out += self._generateTableHead(termin)
        out += self._generateTableItems(termin)
        out += self._generateTableClosing()
        return out

    def _generateTableHead(self, termin):
        out = '<table>' + "\n"
        out += self.tab() + "<tr>" + "\n"
        out += self.tab(2) + '<td style="text-align:right" width="140">' + daymonth(termin['StartDatum'])
        if termin["EndDatum"]:
            out += " - " + daymonth(termin["EndDatum"])
        out += "</td>\n"
        out += self.tab(2) + f'<th style="text-align:left; padding: 0 0 0 20px"> {termin["Fahrtname"]}</th>\n'
        out += self.tab() + "</tr>" + "\n"
        return out

    def _generateTableItems(self, termin):
        out = self.tab() + "<tr>" + "\n"
        out += self.tab(2) + '<td style="text-align: right; vertical-align: top;">' + "\n"
        out += self.tab(3) + '<ul>' + "\n"
        out += self.tab(4) + '<li style="list-style-type:none">'
        if termin['Startzeit'] and termin['Endzeit']:
            out += f"{termin['Startzeit']} - {termin['Endzeit']}"
        elif termin['Startzeit']:
            out += f"ab {termin['Startzeit']}"
        out += '</li>' + "\n"
        out += self.tab(3) + "</ul>" + "\n"
        out += "</td>" + "\n"
        out += self.tab(2) + "<td>" + "\n"
        if termin['PrintFliesstext']:
            out += self.tab(3) + termin['PrintFliesstext'] + "\n"
        out += self.tab(3) + '<ul style="padding-left: 80px">' + "\n"
        ansprechpartner, ansprechpartnerKcw = self._getAnsprechpartner(termin)
        out += self.tab(4) + self._getSurrounding("li", ansprechpartner) + "\n"
        if ansprechpartnerKcw:
            out += self.tab(4) + self._getSurrounding("li", ansprechpartnerKcw) + "\n"
        if termin['Printitems']:
            for item in termin['Printitems']:
                out += self.tab(4) + self._getSurrounding("li", item) + "\n"
        out += self.tab(3) + "</ul>" + "\n"
        out += self.tab(2) + "</td>" + "\n"
        out += self.tab() + "</tr>" + "\n"
        return out

    def _getAnsprechpartner(self, termin):
        ansprechpartner = None
        ansprechpartnerKcw = None
        if termin['Ansprechpartner'] not in self._personsListe:
            ansprechpartner = '<h1 style="color:red">Ansprechpartner nicht in Ansprechpartner Liste gefunden</h1>'
        if termin['AnsprechpartnerKCW'] and (termin['AnsprechpartnerKCW'] not in self._personsListe):
            ansprechpartnerKcw = '<h1 style="color:red">Ansprechpartner nicht in Ansprechpartner Liste gefunden</h1>'
        for item in self._personsListe:
            if termin['Ansprechpartner'] in item:
                ansprechpartner = self._formatAnsprechpartner(item)
        if "AnsprechpartnerKCW" in termin:
            for item in self._personsListe:
                if termin['AnsprechpartnerKCW'] in item:
                    ansprechpartnerKcw = self._formatAnsprechpartner(item)
        return ansprechpartner, ansprechpartnerKcw

    def _formatAnsprechpartner(self, ansprechpartner):
        if ansprechpartner[2] == "w":
            anOut = "Ansprechpartnerin: "
        else:
            anOut = "Ansprechpartner: "
        anOut += f'<a href="mailto:{ansprechpartner[1]}">{ansprechpartner[0]}</a>'
        return anOut

    def _generateTableClosing(self):
        out = "</table>\n"
        return out

    def _writeToFiles(self, spartenListe, head, spartenBodys, foot):
        for index, sparte in enumerate(spartenListe):
            filename = self._filename + f"-{sparte}.html"
            with open(filename, 'w') as file:
                file.write(head)
                file.write(spartenBodys[index])
                file.write(foot)



class ExportIcs(Export):

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
        event.add('dtstart', self.getdate("Start", number))
        event.add('dtend', self.getdate("End", number))
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

    def getdate(self, type, number):
        """
        If startzeit but no endzeit just assume 4 hours
        Names not working
        """

        date = self.termineliste[number][f'{type}Datum']
        zeit = self.termineliste[number][f'{type}zeit']

        if zeit and not date:
            date = self.termineliste[number][f'StartDatum']
            date = datetime.datetime(date.year, date.month, date.day, zeit.hour, zeit.minute, 0)  # , tzinfo=pytz.utc)
            return date
        elif zeit:
            date = datetime.datetime(date.year, date.month, date.day, zeit.hour, zeit.minute, 0)  # , tzinfo=pytz.utc)
            return date
        elif date:
            return datetime.datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=pytz.utc)
        else:
            date = self.termineliste[number][f'StartDatum']
            date += datetime.timedelta(days=1)
            return datetime.datetime(date.year, date.month, date.day, 0, 0, 0, tzinfo=pytz.utc)
