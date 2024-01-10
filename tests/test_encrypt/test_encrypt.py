import os
import pytest
import shutil
from kdna.encrypt import encrypt

DATA_PATH = "tests/data"


def gen_file_structure_bin(nb_files: int = 10) -> dict:
    file_and_content = {}
    print(os.getcwd())
    print(os.listdir(DATA_PATH))
    os.mkdir(DATA_PATH+"/test")

    for k in range(0, nb_files):
        with open(f"{DATA_PATH}/test/test{k}.txt", "w") as test_file:
            file_and_content[f"test{k}.txt"] = f"Hello World : {k}!"
            test_file.write(f"Hello World : {k}!")

    return file_and_content


def gen_deeper_file_structure_bin(nb_files: int = 10) -> dict:
    print(os.getcwd())
    os.mkdir(DATA_PATH+"/test")
    os.mkdir(DATA_PATH+"/test/test")

    file_and_content = {}

    path = DATA_PATH+"/test/"
    for k in range(0, nb_files):
        if int(nb_files / 2) == k:
            path += "test/"
        with open(f"{path}/test{k}.txt", "w") as test_file:
            file_and_content[f"test{k}.txt"] = f"Hello World : {k}!"
            test_file.write(f"Hello World : {k}!")

    return file_and_content


def delete_file_structure():
    print(os.getcwd())
    shutil.rmtree(DATA_PATH+"/test")


@pytest.fixture(autouse=True)
def clean_after_test():
    yield
    try:
        delete_file_structure()
    except FileNotFoundError:
        pass


@pytest.mark.skip(reason="Not implemented yet")
def test_backup():
    gen_file_structure_bin()
    file_out = encrypt.package(
        DATA_PATH+"/test", "backup", DATA_PATH+"/test/backup", False)
    assert os.path.exists(file_out)
    assert file_out == DATA_PATH+"/test/backup.tar.gz"
    os.remove(DATA_PATH+"/test/backup.tar.gz")


@pytest.mark.skip(reason="Not implemented yet")
def test_backup_encrypted():
    gen_file_structure_bin()
    file_out = encrypt.package(
        DATA_PATH+"/test", "backup", DATA_PATH+"/test/backup", True)
    print(file_out)
    assert os.path.exists(file_out)
    assert file_out == DATA_PATH+"/test/backup.enc"
    os.remove(DATA_PATH+"/test/backup.enc")


@pytest.mark.skip(reason="Not implemented yet")
def test_backup_decrypted():
    backup_content = gen_file_structure_bin()
    file_out = encrypt.package(
        DATA_PATH+"/test", "backup", DATA_PATH+"/test/backup", True)
    restore_out = encrypt.restore(file_out,
                                  DATA_PATH+"/test/backup_decrypted", True)
    print("restore_out = " + restore_out)
    assert os.path.exists(restore_out)
    assert restore_out == DATA_PATH+"/test/backup_decrypted/test/backup"
    for file in backup_content:
        with open(restore_out+"/"+file, "r") as f:
            assert f.read() == backup_content[file]


@pytest.mark.skip(reason="Not implemented yet")
def test_backup_encrypted_deeper():
    gen_deeper_file_structure_bin()
    file_out = encrypt.package(
        DATA_PATH+"/test", DATA_PATH+"/test/backup", True)
    print(file_out)
    assert os.path.exists(file_out)
    assert file_out == DATA_PATH+"/test/backup.enc"
    os.remove(DATA_PATH+"/test/backup.enc")


@pytest.mark.skip(reason="Not implemented yet")
def test_backup_decrypted_deeper():
    backup_content = gen_deeper_file_structure_bin()
    file_out = encrypt.package(
        DATA_PATH+"/test", DATA_PATH+"/test/backup", True)
    restore_out = encrypt.restore(file_out,
                                  DATA_PATH+"/test/backup_decrypted", True)
    print("restore_out = " + restore_out)
    assert os.path.exists(restore_out)
    assert restore_out == DATA_PATH+"/test/backup_decrypted/tests/data/test"
    for file in backup_content:
        with open(restore_out+"/"+file, "r") as f:
            assert f.read() == backup_content[file]
