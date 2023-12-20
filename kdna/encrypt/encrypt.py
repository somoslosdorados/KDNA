"""
This module contains encryption functions.

:author: RADULESCU Tristan-Mihai, TCHILINGUIRIAN Théo
:email: <placeholder>, theo.tchlx@gmail.com
:date: 2023-12-15
"""
import os
import tarfile
from cryptography.fernet import Fernet


kdna_default_path = os.path.join(os.path.expanduser('~'), '.kdna/key.key')
kdna_path_to_path = os.path.join(os.path.expanduser('~'), '.kdna/path')


def generate_key(key_path: str = kdna_default_path) -> str:
    """
    Generate a key and save it into a file
    :param key_path: path to the key file
    :return: path to the key file
    """
    if not os.path.exists(os.path.join(os.path.expanduser('~'), '.kdna')):
        os.mkdir(os.path.join(os.path.expanduser('~'), '.kdna'))

    if key_path != kdna_default_path:
        with open(kdna_path_to_path, 'w') as file:
            file.write(os.path.join(os.getcwd(), key_path))

    key = Fernet.generate_key()
    file = open(key_path, 'wb')
    file.write(key)
    file.close()
    return key_path


def load_key() -> bytes:
    """
    Load the previously generated key
    :param key_path: path to the key file
    :return: key as bytes
    """
    key_path = os.path.join(os.path.expanduser('~'), '.kdna/key.key')
    if os.path.exists(kdna_path_to_path):
        with open(kdna_path_to_path, 'r') as file:
            key_path = file.read()

    with open(key_path, 'rb') as file:
        key = file.read()
    return key


def backup(path: str, out: str, encrypt: bool) -> str:
    """
    :param path: path to folder to backup
    :param out: path to output file
    :param encrypt: encrypt the file if True then the output
    file will be a .enc file else it will be a .tar.gz file
    :return: path to output file
    """

    if encrypt:
        with tarfile.open(out+"_temp.tar.gz", "w:gz") as tar:
            tar.add(path)
        cypher(out+"_temp.tar.gz", out+".enc")
        os.remove(out+"_temp.tar.gz")
        return out+".tar.gz"
    with tarfile.open(out+".tar.gz", "w:gz") as tar:
        tar.add(path)

    return out+".tar.gz"


def restore(path: str, out: str) -> str:
    """
    :param path: path to .tar.gz or .enc file to restore
    :param out: path to output folder
    :param encrypted: is the file encrypted
    :return: path to output folder
    """
    encrypted = path.endswith(".enc")
    tar_name = path
    if encrypted:
        decypher(path, out+".tar.gz")
        tar_name = out+".tar.gz"
    file = tarfile.open(tar_name, "r:gz")
    file.extractall(out)
    return out+"/"+file.getnames()[0]


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
        f_out.write(encrypted)
    return encrypted


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
        decrypted = fer.decrypt(data)
        f_out.write(decrypted)
