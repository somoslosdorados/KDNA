"""
This module contains encryption functions.

:author: RADULESCU Tristan-Mihai, TCHILINGUIRIAN Théo
:email: <placeholder>, theo.tchlx@gmail.com
:date: 2023-12-15
"""


import os
import shutil
from cryptography.fernet import Fernet


def generate_key():
    key = Fernet.generate_key()
    file = open('key.key', 'wb')
    file.write(key)
    file.close()


def load_key():
    file = open('key.key', 'rb')
    key = file.read()
    file.close()
    return key


def cypher(path: str, out: str) -> bytes:
    """
    :param path: path to file to encrypt
    :param out: path to output file
    """
    key = load_key()
    fer = Fernet(key)
    with open(path, "rb") as f_in, open(out, "wb") as f_out:
        data = f_in.read()

        encrypted = fer.encrypt(data)
        print(encrypted)

        f_out.write(encrypted)
    return encrypted


def cypher_folders(path: str, out: str):
    """
    :param path: path to folder to encrypt
    :param out: path to output folder
    """
    shutil.copytree(path, out)  # copy folder to then encrypt it
    for dirpath, dirnames, filenames in os.walk(out):
        for filename in filenames:
            cypher(os.path.join(dirpath, filename),
                   os.path.join(dirpath, filename))


def decypher_folders(path: str, out: str):
    """
    :param path: path to folder to decrypt
    :param out: path to output folder
    """
    shutil.copytree(path, out)  # copy folder to then encrypt it
    for dirpath, dirnames, filenames in os.walk(out):
        for filename in filenames:
            decypher(os.path.join(dirpath, filename),
                     os.path.join(dirpath, filename))


def backup(path: str, out: str):
    shutil.copytree(path, out)  # copy folder to then encrypt it
    cypher_folders(path, out)  # encrypt folder
    shutil.make_archive(out, 'zip', out)  # zip folder
    shutil.rmtree(out)  # remove folder


def restore(path: str, out: str):
    shutil.unpack_archive(path, out+"_temp")  # unzip folder
    decypher_folders(out+"_temp", out)  # decrypt folder
    os.remove(path)
    shutil.rmtree(out+"_temp")  # remove folder


def decypher(path: str, out: str):
    """
    :param path: path to file to decrypt
    :param out: path to output file
    """
    key = load_key()
    fer = Fernet(key)
    with open(path, "rb") as f_in:
        data = f_in.read()

    with open(out, "wb") as f_out:
        print(data)
        decrypted = fer.decrypt(data)
        print(decrypted)
        f_out.write(decrypted)
