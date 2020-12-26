from api.file import File
from time import strftime, gmtime
from datetime import datetime

"""
Dette er et eksempel på hvordan rammeverket kan bli implementert. Du kan kjøre filen som den er, gitt at du har installert modulene i requirements.txt og har git installert på maskinen
"""

class Bakery:

    def __init__(self, name, key_path=None, path=None):
        self.name = name
        self.file = File()
        if key_path is not None:
            self.file.set_keypath(key_path)
        else:
            self.generate_key()
        year = strftime("%Y")
        month = strftime("%B")
        week = strftime("week-%V")
        day = strftime("%A")
        self.default_path = False
        if path is None:
            path = f'{self.file.root_directory}/{name}/{year}/{week}/{day}'
            self.default_path = True
        self.path_indices = {'name': -5, 'year': -4, 'year': -3, 'week': -2, 'day': -1}
        self.file.config['path'] = path
        self.file.create_directories()

        # Create a file to hold the date in dateform (makes it possible to search by date instead of year/week/day
        now = datetime.now()
        date = now.strftime("%d-%m-%Y")
        self.file.filename = date
        self.file.contents = ""
        self.file.save()
    
    # Er bare her for å gjøre det lettere å kjøre uten noe oppsett 
    def generate_key(self):
        self.file.new_key('demo')

    def add_file(self, filename, contents, commit_message=None, tag=None):
        self.file.filename = filename
        self.file.contents = contents
        self.file.save(commit_message=commit_message, branch=tag)

    def read_file(self, filename):
        self.file.read(self.file.config['path'] + '/' + filename)
        return self.file.contents

    def change_day(self, day):
        self.change_path(day, self.path_indices['day'])

    def change_week(self, week):
        self.change_path(week, self.path_indices['week'])

    def change_year(self, year):
        self.change_path(year, self.path_indices['year'])

    def change_name(self, name):
        self.change_path(name, self.path_indices['name'])

    def change_path(self, new_value, index):
        if not self.default_path:
            return 'Cannot change week when the format is unknown (needs to be default)'
        # Her splitter vi path opp i en liste, endrer på verdien vi ønsker og gjør det om til en string i path format igjen
        path_split = self.file.config['path'].split('/')
        path_split[index] = new_value
        self.file.config['path'] = '/'.join(path_split)

b = Bakery("demo")
# Oppretter en fil uten noen tag
b.add_file("Produksjon", "Produksjon i dag: 5 boller, 3 brød og 14 kanelsnurrer")
# Lagrer en oppskrift med en tag, her oppskrift. Vi bruker git branches. Idéen er at man bruker branches som "emneknagg", sortere etter grunnoppskrift osv
b.add_file("Brodoppskrift", "500 kg sukker og 3 egg", tag="Oppskrifter")
b.add_file("Timeliste_Jens", "10 timer", tag="Timelister")

print("\n####\n")
print(b.read_file('Produksjon'))

