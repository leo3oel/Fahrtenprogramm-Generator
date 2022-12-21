def appenddictionarylist(liste, inSparte, inSpartennr, inStartDatum, inAnsprechpartner, inItems, inFahrtname, inEndDatum=None, inStartzeit=None, inEndzeit=None):
    liste.append({
        'Sparte' : inSparte,
        'Spartennr' : inSpartennr,
        'Fahrtname' : inFahrtname,
        'Startzeit' : inStartzeit,
        'Endzeit' : inEndzeit,
        'StartDatum' : inStartDatum,
        'EndDatum' : inEndDatum,
        'Ansprechpartner' : inAnsprechpartner, # 2D-Liste mit Ansprechpartner, Email. Wenn Länge>1: Ansprechpartner, Ansprechpartner KCW, Ansprechpartner n
        'items' : inItems # Liste mit Stichpunkten
    })
    return liste


def texport(terminefilename, preamble, filenameOut, bemerkungenvorneweg=None):
    '''
    Exports a list of dictionarys into a tex file, needs to import a preamble
    '''

    # Sort List by Date
    terminefilename = sorted(terminefilename, key=lambda i: i['StartDatum'])

    # Make List of Sparten
    spartenliste = []
    for Fahrt in terminefilename:
        if Fahrt['Sparte'] not in spartenliste:
            spartenliste.insert(Fahrt['Spartennr'], Fahrt['Sparte'])

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
                    if (Fahrt["EndDatum"] != None and Fahrt["Startzeit"] != None and Fahrt["Endzeit"] != None):
                        texfile.write(str(Fahrt['StartDatum']) + " - " + str(Fahrt["EndDatum"]) +"\\")
                        texfile.write(Fahrt['Startzeit'] - Fahrt['Endzeit'])
                    elif (Fahrt["EndDatum"] and Fahrt["Startzeit"]):
                        texfile.write(str(Fahrt['StartDatum']) + " - " + str(Fahrt["EndDatum"]) +"\\")
                        texfile.write("ab " + Fahrt['Startzeit'])
                    elif Fahrt["EndDatum"] and Fahrt["Startzeit"] == None and Fahrt["Endzeit"] == None:
                        texfile.write(str(Fahrt['StartDatum']) + " - " + str(Fahrt["EndDatum"]))
                    else:
                        texfile.write(str(Fahrt['StartDatum']))
                    texfile.write("}\n")

                    # Print items
                    texfile.write("\\begin{itemize}\n")
                    texfile.write("    \\item Ansprechpartner: " + Fahrt['Ansprechpartner'][0] + " \\href{"+Fahrt['Ansprechpartner'][1] + "}{" + "mailto:"  + Fahrt['Ansprechpartner'][1] + "}\n")
                    for item in Fahrt['items']:
                        texfile.write("    \\item " + item + "\n")
                    texfile.write("\\end{itemize}\n\n")
            texfile.write("\n")
        texfile.write("\\end{document}")
    return(spartenliste)

# Define Basics
ansprechpartner = [
    ['Leo', 'sport@kc-wuerzburg.de'],
    ['Sebastian', 'wildwasser@kc-wuerzburg.de'],
    ['Julia', 'jugend@kc-wuerzburg.de']
]
terminedic = []

# Append Terminelist
appenddictionarylist(
    liste = terminedic,
    inSparte = 'Allgemein',
    inFahrtname = "Arbeitsdienst",
    inSpartennr = 0,
    inStartDatum = 20230101,
    inAnsprechpartner = ansprechpartner[0],
    inStartzeit= "9:30",
    inItems = ["Beispiel 1", "Text"]
)
appenddictionarylist(
    liste = terminedic,
    inSparte = 'Jugend',
    inFahrtname = "irgendwas für die jugend",
    inSpartennr = 1,
    inStartDatum = 20230304,
    inEndDatum = 20230307,
    inAnsprechpartner = ansprechpartner[2],
    inItems = ["Beispiel 2", "Text"]
)
appenddictionarylist(
    liste = terminedic,
    inSparte = 'Kanupolo',
    inFahrtname = "Boote flicken",
    inSpartennr = 2,
    inStartDatum = 202303016,
    inStartzeit='15:00',
    inEndzeit='19:00',
    inAnsprechpartner = ansprechpartner[0],
    inItems = ["Boote flicken"]
)
appenddictionarylist(
    liste = terminedic,
    inSparte = 'Jugend',
    inFahrtname = "irgendwas für die jugend",
    inSpartennr = 1,
    inStartDatum = 20230304,
    inEndDatum = 20230307,
    inAnsprechpartner = ansprechpartner[2],
    inItems = ["Beispiel 2", "Text"]
)


print(texport(terminedic, "preamble.tex", "test.tex"))