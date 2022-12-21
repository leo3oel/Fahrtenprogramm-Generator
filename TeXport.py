def appenddictionarylist(liste, inSparte, inSpartennr, inStartDatum, inAnsprechpartner, inItems, inEndDatum=None):
    liste.append({
        'Sparte' : inSparte,
        'Spartennr' : inSpartennr,
        'StartDatum' : inStartDatum,
        'EndDatum' : inEndDatum,
        'Ansprechpartner' : inAnsprechpartner, # 2D-Liste mit Ansprechpartner, Email. Wenn Länge>1: Ansprechpartner, Ansprechpartner KCW, Ansprechpartner n
        'items' : inItems # Liste mit Stichpunkten
    })
    return liste


def texport(terminefilename, preamble):
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

    # Print out TeX
    for Fahrt in terminefilename:
        print(Fahrt['Sparte'])
        print(str(Fahrt['StartDatum']) + " - " + str(Fahrt["EndDatum"]))
        print(Fahrt['Ansprechpartner'][0] + " \\hyperlink{"+Fahrt['Ansprechpartner'][1] + "}{" + "mailto:"  + Fahrt['Ansprechpartner'][1] + "}")
        for item in Fahrt['items']:
            print("\\item " + item)
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
    inSpartennr = 0,
    inStartDatum = 20230101,
    inAnsprechpartner = ansprechpartner[0],
    inItems = ["Beispiel 1", "Text"]
)
appenddictionarylist(
    liste = terminedic,
    inSparte = 'Jugend',
    inSpartennr = 1,
    inStartDatum = 20230304,
    inEndDatum = 20230307,
    inAnsprechpartner = ansprechpartner[2],
    inItems = ["Beispiel 2", "Text"]
)

print(texport(terminedic, 0))