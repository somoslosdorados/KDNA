from fabric import Connection

def upload_file(connection: Connection, local_path: str, remote_path: str) -> None:
    """
    Send a file on a specific path in the remote server. Might throw an exception.
    """
    connection.put(local_path, remote=remote_path)

def download_file(connection: Connection, local_path: str, remote_path: str) -> None:
    """
    Receive a file on a specific path from the remote server. Might throw an exception.
    """
    connection.get(remote_path, local=local_path)

def main ():
    with Connection("bbronsin@162.38.112.136") as c:
        upload_file(c, "/toto.txt", "/home/bbronsin/")
        download_file(c, "/home/baptiste/", "/home/bbronsin/toto1.txt")

if __name__ == '__main__':
    main()