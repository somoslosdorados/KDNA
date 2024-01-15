"""This module contains encryption functions.
:author: RADULESCU Tristan-Mihai, TCHILINGUIRIAN Théo
:email: <placeholder>, theo.tchlx@gmail.com
:date: 2023-12-15
"""
import os
import tarfile
from cryptography.fernet import Fernet

from kdna.logger.logger import log


kdna_default_path = os.path.join(os.path.expanduser('~'), '.kdna/key.key')
kdna_path_to_path = os.path.join(os.path.expanduser('~'), '.kdna/path')


def generate_key(key_path: str = kdna_default_path) -> str:
    """Generate a key and save it into a file
    :param key_path: path to the key file
    :return: path to the key file
    """
    if not os.path.exists(os.path.join(os.path.expanduser('~'), '.kdna')):
        os.mkdir(os.path.join(os.path.expanduser('~'), '.kdna'))

    if key_path != kdna_default_path:
        with open(kdna_path_to_path, 'w', encoding='utf-8') as file:
            file.write(os.path.join(os.getcwd(), key_path))

    key = Fernet.generate_key()
    with open(key_path, 'wb') as file:
        file.write(key)
    return key_path


def load_key() -> bytes:
    """Load the previously generated key
    :param key_path: path to the key file
    :return: key as bytes
    """
    key_path = os.path.join(os.path.expanduser('~'), '.kdna/key.key')
    if os.path.exists(kdna_path_to_path):
        with open(kdna_path_to_path, 'r', encoding='utf-8') as file:
            key_path = file.read()

    with open(key_path, 'rb') as file:
        key = file.read()
    return key


def package(path: str, name: str, out: str, encrypt: bool) -> str:
    """:param path: path to folder to backup
    :param out: path to output file
    :param encrypt: encrypt the file if True then the output file will be a .enc file else it will be a .tar.gz file
    :return: path to output file
    """
    old_path = os.path.abspath(os.getcwd())
    abs_out = os.path.join(os.path.abspath(out), name + ".tar.gz")
    abs_enc_out = os.path.join(os.path.abspath(out), name + ".enc")
    os.chdir(path)  # go to the folder to backup
    with tarfile.open(abs_out, "w:gz") as tar:
        tar.add('.')
    if encrypt:
        cypher(abs_out, abs_enc_out)
        os.remove(abs_out)
        os.chdir(old_path)
        return name+".enc"
    os.chdir(old_path)
    return name+".tar.gz"


def restore(path: str, out: str) -> str:
    """:param path: path to .tar.gz or .enc file to restore
    :param out: path to output folder
    :param encrypted: is the file encrypted
    :return: path to output folder
    """
    print("restoring = ", path)
    log("INFO", "restoring = "+ path)
    encrypted = path.endswith(".enc")
    tar_name = path
    if encrypted:
        decypher(path, out+".tar.gz")
        tar_name = out+".tar.gz"
    file_name = ""
    with tarfile.open(tar_name, "r:gz") as file:
        file.extractall(out)
        file_name = file.getnames()[0]
    return out+"/"+file_name


def cypher(path: str, out: str) -> bytes:
    """:param path: path to file to encrypt
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
    """:param path: path to file to decrypt
    :param out: path to output file
    """
    key = load_key()
    fer = Fernet(key)
    with open(path, "rb") as f_in:
        data = f_in.read()

    with open(out, "wb") as f_out:
        decrypted = fer.decrypt(data)
        f_out.write(decrypted)
