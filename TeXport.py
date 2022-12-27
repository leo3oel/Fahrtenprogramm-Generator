import datetime
import subprocess
from DateTime import daymonthyear
from DateTime import daymonth



def makepdfanddisplay(filename):
    subprocess.run(["lualatex", filename])
    subprocess.run(["lualatex", filename])
    subprocess.Popen(["zathura", filename[:-3]+"pdf"])


def structurizelist(list):
    
    # Sort List by Date
    list = sorted(list, key=lambda i: i['StartDatum'])

    """ # Make List of Sparten
    spartenliste = []
    for fahrt in list:
        if fahrt['Sparte'] not in spartenliste:
            spartenliste.insert(fahrt['Spartennr'], fahrt['Sparte'])
    return spartenliste """


def texport(terminefilename, spartenlisteold, preamble, filenameOut, bemerkungenvorneweg=None):
    '''
    Exports a list of dictionarys into a tex file, needs to import a preamble
    '''
    spartenliste = spartenlisteold
    structurizelist(terminefilename)

    # Read in Preamble
    with open(preamble) as inpreamble:
        preamble = inpreamble.read()

    # Mark hyperlinks APPEND DICTIONARY
    for fahrt in terminefilename:
        list = []
        for item in range(len(fahrt['items'])):
            list.append(markhyperlinks(fahrt['items'][item]))
        dict1 = {'PrintFließtext': markhyperlinks(fahrt['Fließtext']), 'Printitems': list}
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

                    # Print Fließtext
                    if(Fahrt['PrintFließtext']):
                        texfile.write("\\mbox{}\\\\\\mbox{}"+Fahrt['Fließtext'])

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
                    if Fahrt['Printitems']:
                        for item in Fahrt['Printitems']:
                            texfile.write("    \\item " + item + "\n")
                    texfile.write("\\end{itemize}\n\n")
            texfile.write("\n")
        texfile.write("\\end{document}")

    for fahrt in terminefilename:
        fahrt.pop("Printitems")
        fahrt.pop('PrintFließtext')


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
    outputstring += currentword
    return outputstring

def clearfliesstext(dict):
    """
    Deltes \n at the end
    """

    for dic in dict:
        string = dic['Fließtext']
        if string:
            char = string[-1]
            while char == "\n":
                string = string[:-1]
                char = string[-1]
            dic['Fließtext'] = string