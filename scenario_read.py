from api.file import File
import os


#Henter ut current working directory
directory = os.getcwd()

file = File()
file.set_keypath(directory + '/key.asc')
file.read(directory + '/scenarios/scenario1')
print(file.contents)
