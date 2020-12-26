from api.file import File

file = File()
file.filename = "scenario1"
file.title = "test.txt"
file.contents = "Dette er en test"


file.new_key("testkey")

file.config['path'] =  f'{file.root_directory}/scenarios/'
file.create_directories()
file.save()



