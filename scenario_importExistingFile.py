from api.file import File
import os
import getpass


#Modul som henter ut brukernavn. Brukes for å vise at man kan importere fra en user folder
user = getpass.getuser()

file=File()
file.create_directories()
directory = os.getcwd()

file.set_keypath(directory + '/key.asc')
file.import_existing('/home/' + user + '/importTest')
