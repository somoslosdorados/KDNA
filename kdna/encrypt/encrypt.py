import pyzipper

secret_password = b'password'


def encrypt_archive(file_name: str):
    with pyzipper.AESZipFile(file_name,
                             'w',
                             compression=pyzipper.ZIP_LZMA,
                             encryption=pyzipper.WZ_AES) as zf:
        zf.setpassword(secret_password)
        zf.write(file_name)


def decrypt_archive(file_name: str):
    with pyzipper.AESZipFile(file_name, 'r') as zf:
        zf.setpassword(secret_password)
        zf.extractall()
