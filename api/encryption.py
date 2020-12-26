import pgpy
import typing
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm, CompressionAlgorithm
class Encryption:
        """
            This class handles encryption and decryption of contents. It uses PGPy to handle operations for encryption/decryption.
            Currently does not support password protected keys
        """
        def __init__(self, key: pgpy.PGPKey=None):  
            """ Initialize a new object. Optional parameter for key """
            self.key = key

        def new_key(self, name: str, comment: str=None, email: str=None, flags: dict=None, hashes: list=None, ciphers: list=None, compression: list=None):
            """ Creates a new PGP key. Currently does not support creating 'subkeys' """
            self.key = pgpy.PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 4096)
            uid = pgpy.PGPUID.new(name, comment=comment, email=email)
            if flags is None:
                flags = {KeyFlags.Sign, KeyFlags.EncryptCommunications, KeyFlags.EncryptStorage}
            if hashes is None:
                hashes = [HashAlgorithm.SHA256, HashAlgorithm.SHA512]
            if ciphers is None:
                ciphers = [SymmetricKeyAlgorithm.AES256, SymmetricKeyAlgorithm.AES128]
            if compression is None:
                compression = [CompressionAlgorithm.BZ2, CompressionAlgorithm.Uncompressed]
            self.key.add_uid(uid, usage=flags, hashes=hashes, ciphers=ciphers, compression=compression)
            self.pubkey = self.key.pubkey
            self.save_key(name)

        def save_key(self, name):
            """
                Saves PGP key to disk. 
                Creates one file for the private key, and one for the public key.
                Saves in ASCII format to current directory.
                Not meant to be called on by user, but it can be
            """
            filename = name.replace(" ", "")
            keystr = str(self.key)
            pub = str(self.key.pubkey)
            with open(f'{filename}.asc', 'w') as f:
                f.write(keystr)
            with open(f'{filename}.pub', 'w') as f:
                f.write(pub)
            print("Keys saved to running directory. Please move the private key (*.asc) to a more secure place")

        def load_key(self, path: str):
            """ Loads PGP key from disk """
            key, _ = pgpy.PGPKey.from_file(path)
            key.compression = [CompressionAlgorithm.BZ2]
            self.key = key
            self.pubkey = key.pubkey

        def encrypt(self, content: str):
            """ Encrypts the contents of the file and returns it """
            content = pgpy.PGPMessage.new(content, file=True)
            encrypted = self.pubkey.encrypt(content)
            return encrypted

        def decrypt(self, encrypted: str):
            """ Decrypts the contents of a string and returns the message (content) of the PGP message """
            if self.key is None or self.key.is_public:
                raise NoPrivateKeyError("There is no private key loaded. It is needed to decrypt messages")
            content = pgpy.PGPMessage.from_blob(encrypted) 
            decrypt = self.key.decrypt(content)
            return str(decrypt.message) 


class NoPrivateKeyError(Exception):
    """ Exception that is raised if you try to decrypt something with no private key set """
    def __init__(self, message):
        super().__init__(message)


