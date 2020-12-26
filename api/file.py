import os
from .filesystem import Filesystem

class File(Filesystem):
    """
        Class that handles the basics of files. It holds filenames and contents. 
        Inherits from Filesystem, so everything can be done from this class, which is the point of its simplicity
    """
    def __init__(self, key_path=None, filename=None, contents=None):
        """ Parameters are optional to avoid confusion """
        self.filename = filename
        self.contents = contents
        self.key_path = key_path
        super().__init__()
        if key_path is not None:
            super().set_keypath(self.key_path)
    
    def save(self, commit_message=None, branch=None):
        """ Checks if filename and contents is set, saves file and clears content of the object """
        if self.filename is None:
            raise ValueError('File has no filename') 
        if self.contents is None:
            raise ValueError('File has no contents')
        success = self.save_file(self, commit_message, branch)
        # Etter lagret så clearer vi variablene  
        if success:
            self.clear()
            return True

    def clear(self):
        """ Clears filename and contents from instance """
        self.filename = None
        self.contents = None

    def read(self, path, branch=None):
        """ Sets filename and contents for instance of file object. """  
        if branch:
            self.change_branch(branch)
        with open(path) as f:
            encrypted_data = f.read()
        decrypted_data = self.decrypt(encrypted_data)
        filename = os.path.split(path)[1]
        self.filename = filename
        self.contents = decrypted_data 
        self.change_branch('master')
        return self

    def import_existing(self, path, new_name=None, branch=None):
        """ Import an existing plaintext file into the system. Will keep filename and encrypt with predefined PGP key. """
        if branch:
            self.change_branch(branch)
        with open(path) as f:
            plain = f.read()
        if new_name is None:
            new_name = os.path.split(path)[1]
        filename = new_name
        self.filename = filename
        self.contents = plain
        self.save()
        self.change_branch('master')

