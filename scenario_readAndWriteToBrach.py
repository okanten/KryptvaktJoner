from api.file import File

file = File()
file.filename = "scenario5"
file.title = "test.txt"
file.contents = "Dette er en test tjoho"


file.new_key("testkey")

file.config['path'] =  f'{file.root_directory}/scenarios/'
file.create_directories()
file.save(branch='testBranch')



file.read(file.config['path'] + 'scenario5', branch='testBranch')
print(file.contents)
