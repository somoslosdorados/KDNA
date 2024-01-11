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
    connection.get(local_path, remote=remote_path)


def main():
    with Connection("bbronsin@168.38.112.136") as c:
        upload_file(c, "/home/baptiste/Bureau/toto.txt", "/kdna/projet1/")


if __name__ == '__main__':
    main()
