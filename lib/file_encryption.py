#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""File encryption for ostackrc variables."""
import base64
import getpass
import os
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class FileEncryption(object):
    """File Encryption.

    later to implement:
        https://github.com/edwardspeyer/sshovel/blob/master/sshovel
        encrypt and decrypt with ssh-agent
    """
    key = None

    def __init__(self):
        pass

    def generate_key(self, password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        print(
            "{ds}\n# YOUR KEY: {k}\n{ds}".format(
                k=key, ds="#" * 30
            )
        )
        return key

    def encrypt_configfile(self, data, output_file, key=None):
        if key is None:
            key = Fernet.generate_key()
        elif key is not None and len(key) != 44:
            print("Wrong key length {length}, encryption process aborted!".format(length=len(key)))
            return None
        
        print(
            "{ds}\n# YOUR KEY: {k}\n{ds}".format(
                k=key, ds="#" * 30
            )
        )

        fernet = Fernet(key)
        encrypted = fernet.encrypt(bytes(data, "utf-8"))

        with open(output_file, "wb") as f:
            f.write(encrypted)

    def decrypt_configfile(self, input_file, key):
        with open(input_file, "rb") as f:
            data = f.read()
   
        try:
            fernet = Fernet(key)
            decrypted = fernet.decrypt(data)
        except Exception as error:
            print("ERROR: {0} (Wrong password.)".format(error))
            sys.exit(1)

        return decrypted


if __name__ == "__main__":

    env = "Ich bin ein Datensatz"
    crypto = FileEncryption()
    crypto.encrypt_configfile(data=env, output_file="test.encrypted")
    """
    crypto = crypt_configfile()
    key = b'1tToKqrpUCiSySkXzlKE3cdI5FN8zJZHCRVYisAU3n8='
    data = crypto.decrypt_configfile(input_file="test.encrypted")
    print("{}".format(data.decode("utf-8")))
    """
