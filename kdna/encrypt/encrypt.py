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


def cyper() -> bytes:
    key = load_key()
    fer = Fernet(key)
    with open("test.txt", "rb") as f:
        data = f.read()

    encrypted = fer.encrypt(data)
    print(encrypted)
    with open("test_cypher.txt", "w") as f:
        f.write(encrypted.decode())
    return encrypted


def decypher():
    key = load_key()
    fer = Fernet(key)
    with open("test_cypher.txt", "r") as f:
        data = f.read()
    decrypted = fer.decrypt(data.encode())
    print(decrypted)
    with open("test_decypher.txt", "wb") as f:
        f.write(decrypted)
