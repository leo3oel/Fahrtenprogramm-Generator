# Fahrtenprogramm_Generator
Programm um Termine einheitlich einzugeben und daraus alle benötigten Formate zu erzeugen
## Features
 - Speichern der Liste als `.json` File. Das gespeicherte File hat zwecks Wiederkennung die Endung `.fahrten`
 - Anlegen, Bearbeiten und Löschen von Terminen
 - Anlegen und Löschen von Sparten
    - LaTeX Datei wird nach Sparten strukturiert
 - Anlegen und Löschen von Ansprechpartnern
    - Ansprechpartner können intern oder extern sein. Bei externen wird zusätzlich nach internen gefragt
 - Output als:
    - HTML (pro Sparte)
    - ICS (gesamt)
    - LaTeX (sortiert nach Sparten und ohne extra Sortierung)
    - PDF (benötigt LaTeX Installation)
