# Fahrtenprogramm_Generator
Python GUI to generate PDFs/HTML/iCal for appointements.

## Setup
 - Install python and poetry
 - Run `poetry install`
 - Run `poetry run python gui.py`

## Usage
 - Enter Information
   - Reponsible People
   - Divisions
   - Appointments
 - Save in `.json`-format (fileending is `.fahrten`)
 - Generate Files
   - HTML (per division)
   - ICS (grouped)
   - LaTeX (per division or grouped)
   - PDF (relies on LaTeX Installation)
