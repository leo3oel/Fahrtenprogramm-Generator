import datetime
import subprocess

def appenddictionarylist(liste, inSparte, inSpartennr, inStartDatum, inAnsprechpartner, inItems, inFahrtname, inFließtext=None,inAnsprechpartnerKCW=None, inEndDatum=None, inStartzeit=None, inEndzeit=None):
    liste.append({
        'Sparte' : inSparte,
        'Spartennr' : inSpartennr,
        'Fahrtname' : inFahrtname,
        'Startzeit' : inStartzeit,
        'Endzeit' : inEndzeit,
        'StartDatum' : inStartDatum,
        'EndDatum' : inEndDatum,
        'Ansprechpartner' : inAnsprechpartner, # 2D-Liste mit Ansprechpartner, Email. Wenn Länge>1: Ansprechpartner, Ansprechpartner KCW, Ansprechpartner n
        'AnsprechpartnerKCW' : inAnsprechpartnerKCW,
        'Fließtext' : inFließtext,
        'items' : inItems # Liste mit Stichpunkten
    })
    return liste


def hourminute(time):
    return "\\footnotesize{"+ "{:02d}".format(time.hour) + ":" + "{:02d}".format(time.minute) + "}"


def daymonth(day):
    return "{:02d}".format(day.day) + "." + "{:02d}".format(day.month)


def makepdfanddisplay(filename):
    subprocess.run(["lualatex", filename])
    subprocess.Popen(["zathura", filename[:-3]+"pdf"])


def structurizelist(list):
    
    # Sort List by Date
    list = sorted(list, key=lambda i: i['StartDatum'])

    # Make List of Sparten
    spartenliste = []
    for Fahrt in list:
        if Fahrt['Sparte'] not in spartenliste:
            spartenliste.insert(Fahrt['Spartennr'], Fahrt['Sparte'])
    return spartenliste


def texport(terminefilename, preamble, filenameOut, bemerkungenvorneweg=None):
    '''
    Exports a list of dictionarys into a tex file, needs to import a preamble
    '''

    spartenliste = structurizelist(terminefilename)

    # Read in Preamble
    with open(preamble) as inpreamble:
        preamble = inpreamble.read()

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
            texfile.write(bemerkungenvorneweg)

        for sparte in spartenliste:
            texfile.write("\\chapter*{")
            texfile.write(sparte + "}\n")
            texfile.write("\\thispagestyle{" + sparte + "}\n" + "\\addcontentsline{toc}{chapter}{\\protect\\numberline{}" + sparte + "}\n")
            texfile.write("\\pagestyle{" + sparte + "}\n")

            for Fahrt in terminefilename:

                if Fahrt['Sparte'] == sparte:
                    
                    # Print Paragraphname
                    texfile.write("\\paragraph{"+Fahrt['Fahrtname']+"}")

                    # Print Marginnote
                    texfile.write("\\marginnote{")
                    if Fahrt["EndDatum"]:
                        texfile.write(daymonth(Fahrt['StartDatum']) + " - " + daymonth(Fahrt["EndDatum"]))
                        if Fahrt["Startzeit"] and Fahrt["Endzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write(hourminute(Fahrt['Startzeit']) + " - " + hourminute(Fahrt['Endzeit']))
                        elif Fahrt["Startzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write("ab " + hourminute(Fahrt['Startzeit']))
                    else:
                        texfile.write(daymonth(Fahrt['StartDatum']))
                        if Fahrt["Startzeit"] and Fahrt["Endzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write(hourminute(Fahrt['Startzeit']) + " - " +  hourminute(Fahrt['Endzeit']))
                        elif Fahrt["Startzeit"]:
                            texfile.write(" \\\\ ")
                            texfile.write("ab " + hourminute(Fahrt['Startzeit']))
                    texfile.write("}\n")

                    # Print Fließtext
                    if(Fahrt['Fließtext']):
                        texfile.write("\mbox{}\\\\\\mbox{}\\\\"+Fahrt['Fließtext'] + "\\\\")

                    # Print items
                    texfile.write("\\begin{itemize}\n")
                    if Fahrt['Ansprechpartner'][2] == 'w':
                        texfile.write("    \\item Ansprechpartnerin: ")
                    else:
                        texfile.write("    \\item Ansprechpartner: ")
                    texfile.write(Fahrt['Ansprechpartner'][0] + " \\href{"+ "mailto:"  +Fahrt['Ansprechpartner'][1] + "}{"+ Fahrt['Ansprechpartner'][1] + "}\n")
                    if(Fahrt['AnsprechpartnerKCW']):
                        if Fahrt['Ansprechpartner'][2] == 'w':
                            texfile.write("    \\item Ansprechpartnerin KCW: ")
                        else:
                            texfile.write("    \\item Ansprechpartner KCW: ")
                        texfile.write(Fahrt['Ansprechpartner'][0] + " \\href{"+ "mailto:"  +Fahrt['Ansprechpartner'][1] + "}{"+ Fahrt['Ansprechpartner'][1] + "}\n")
                    for item in Fahrt['items']:
                        texfile.write("    \\item " + item + "\n")
                    texfile.write("\\end{itemize}\n\n")
            texfile.write("\n")
        texfile.write("\\end{document}")
    return(spartenliste)

terminedic = []

# Define Basics
def testsettings():
    # Name, Mail, geschlecht, KCW?
    ansprechpartner = [
        ['Leo', 'sport@kc-wuerzburg.de', 'm', True],
        ['Sebastian', 'wildwasser@kc-wuerzburg.de', 'm', True],
        ['Julia', 'jugend@kc-wuerzburg.de', 'w', 'True'],
        ['Bernd Sachs', 'wildwasser@kanu-bayern.de', 'w', 'False']
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

testsettings()
texport(terminedic, "preamble.tex", "test.tex")
print("texport ok")
makepdfanddisplay("test.tex")
print("made pdf")