from .encryption import Encryption
import os
import subprocess

class Filesystem(Encryption):
    """ 
        This class handles the actual writing and directory management. Thanks to python its really simple.
        Inherits from Encryption
    """

    def __init__(self, root_directory=None, sub_directory=None):
        """ 
            Optional parameters. Will be set to defaults if not set.
        """
        if root_directory is None:
            root_directory = os.getcwd()
        if sub_directory is None:
            sub_directory = 'encrypted_fs/'
        self.config = dict()
        self.root_directory = root_directory
        self.sub_directory = sub_directory
        self.config['root_directory'] = root_directory
        self.config['sub_directory'] = sub_directory
        self.config['path'] = f'{self.root_directory}/{self.sub_directory}'

    def create_directories(self):
        """ Create directories based on variables root_directory and sub_directory """
        try: 
            # Make directories and initialize git repo
            path = self.config['path']
            os.makedirs(f'{path}', exist_ok=True)
            subprocess.run(['git', 'init', f'{path}'])
            return True
        except OSError:
            return False

    def save_file(self, file, commit_message=None, branch=None):
        """ Calls for encryption of contents and saves file to disk, based on values for root_directory and sub_directory """
        filename = file.filename
        encrypted_contents = self.encrypt(file.contents)

        path = self.config['path'] + '/' + filename
        try:
            with open(f'{path}', 'w') as f:
                f.write(str(encrypted_contents))
        except OSError:
            raise OSError
        if commit_message is None:
            commit_message = 'new file'
        if branch is not None:
            #subprocess.run(['git', 'switch', '-c', f'{branch}'], cwd=self.config['path'])
            self.change_branch(branch)
        subprocess.run(['git', 'add', f'{filename}'], cwd=self.config['path'])
        subprocess.run(['git', 'commit', f'{path}', '-m' f'{commit_message}'], cwd=self.config['path'])
        self.change_branch('master')
        return True

    def set_keypath(self, path):
        """ Dummy function to set a path for PGP key. Calls parent class """
        super().load_key(path)

    def change_branch(self, branch_name):
        path = self.config['path']
        subprocess.run(['git', 'checkout', '-qB', f'{branch_name}'], cwd=path)

