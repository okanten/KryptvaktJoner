from api.file import File
import os
import getpass


#Modul som henter ut brukernavn. Brukes for å vise at man kan importere fra en user folder
user = getpass.getuser()
new_filename = "importedTest"

file=File()
file.create_directories()
directory = os.getcwd()

file.set_keypath(directory + '/key.asc')

# Her importerer vi en fil, og gir den et nytt navn. 
file.import_existing('/home/' + user + '/importTest', new_name=new_filename)
