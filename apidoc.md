# API Documentation

## Encryption Object

class Encryption(key=None)

Parameters: 
- *key* - optional parameter to define key when you initialize the object

### *new_key*(name, comment=None, email=None, flags=None, hashes=None, ciphers=None, compression=None)

Generate a new PGP keypair and call the method which saves to disk.

*Parameters:*
- *name* - Name registered for the keypair as well as used for filename

### *save_key*(name)

Saves the PGP keypair to disk

*Parameters:*
- *name* - The filename of the keypair (eg. name='Key' will be Key.asc and Key.pub)

### *load_key*(path)

Loads key into encryption instance. Can be private+public or just public depending on use-case. This is never meant to be used by the users of the framework, it is used internally within the api

*Parameters:*
- path - Path to the key

### *encrypt*(content)

Encrypts content with the set public key

*Parameters:*
- content - Content to be encrypted

### *decrypt*(encrypted)

Decrypts given content with the set private key. Will throw error if no private key is set. 

*Parameters:*
- encrypted - Encrypted string to be decrypted

### class NoPrivateKeyError(Exception)

Custom excepton that can be raised when no private key is present. Just a standard inherited exception, nothing magical.

## Filesystem Object

class Filesystem(Encryption)

Inherits methods from Encryption class

### *__init__*(root_directory=None, sub_directory=None)

Initializes a new Filesystem object

*Parameters*:
- root_directory - Optional parameter with default values. Sets the first part of the directory to be saved to
- sub_directory - Optional parameter with default values. Sets the second part of the directory to be saved to.

### *create_directories()*

Creates directories based on root_directory and sub_directory. If directories already exists it will ignore it. Also initializes git repository.

### *save_file*(file, commit_message=None, branch=None)

Encrypts filecontent and saves file to disk. Used internally in the API. 

*Parameters*:
- file - file object to be encrypted
- commit_message - Optional parameter. Specifies commit message for git repo
- branch - Optional parameter. Specifies branch

### *set_keypath*(path)

Sets the key path for key to be used. This is the method users of the framework will use.

*Parameters*:
- path - Path to the keyfile to be used. If private key it will load public key as well seeing as it can be derived from a private key.


### change_branch(branch_name)

Changes branch in git repository. Creates branch if it doesnt exist.

*Parameters*:
- branch_name - parameter which defines which branch to switch to.


## File Object

class File(Filesystem)

Inherits from Filesystem

### *__init__*(key_path=None, filename=None, contents=None)

Initializes file object to be used for all calls to the API by the user. Has optional parameters

*Parameters*:
- key_path - Optional parameter to set key path at init
- filename - Optional parameter to set filename at init
- contents - Optional parameter to set file contents at init

### *save*(commit_message=None, branch=None)

Method that will be used by the users of the framework. Checks if the file actually has contents, while still being able to save an empty text string. If saved successfully it clears filename and contents

*Parameters*:
- commit_message - Optional parameter for commit message. Will be passed through to super method
- branch - Optional parameter which switches branch before saving to disk

### *read*(path, branch=None)

Method to read file from filesystem based on path given.

*Parameters*:
- path - Path to file 
- branch - Optional parameter to read from specific branch. Will read from 'master' if none is set.

### *import_existing*(path, new_name=None, branch=None)

Import plaintext file, encrypt it and (optionally) give it a new name

*Parameters*:
- path - path to file to be read from
- new_name - Optional new filename given to file
- branch - Optional branch to save new file to.

