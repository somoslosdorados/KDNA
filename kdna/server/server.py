from fabric import Connection  # type: ignore
from kdna.tags.tags import getFileNameByTag


def directory_exists(connection: Connection, path: str) -> bool:
    """
    Check if a directory exists on the remote server. Might throw an exception.
    """
    return connection.run(f"test -d {path}", warn=True).ok


def upload_file(connection: Connection, local_path: str, remote_path: str) -> None:
    """
    Send a file on a specific path in th/e remote server. Might throw an exception.
    """
    if not directory_exists(connection, remote_path):
        connection.run(f"mkdir -p {remote_path}")

    connection.put(local_path, remote=remote_path)


def download_file(connection: Connection, local_path: str, remote_path: str) -> str:
    """
    Receive a file on a specific path from the remote server. Might throw an exception.
    """
    # check if there is a file like remote_path.enc or remote_path.tar.gz
    files = connection.run(f"ls {remote_path}.*", warn=True).stdout.split("\n")
    if len(files) == 0:
        raise Exception(f"Error: no file found on {remote_path}")
    for file in files:
        file_name = file.split("/")[-1]
        if file_name.endswith(".enc"):
            connection.get(file, local=local_path+".enc")
            return file_name
    connection.get(remote_path, local=local_path+".tar.gz")
    return files[0].split("/")[-1]

# méthode pour trouver le path d'un backup à partir d'un tag et d'un nom de projet


def find_path(connection: Connection, tag: str, project_name: str) -> str:
    """
    Find a path in the remote server. Might throw an exception.
    """

    # vérifier que le dossier du projet existe
    try:
        connection.run(f"ls ./kdna/{project_name}")
    except Exception:
        raise Exception(f"Project {project_name} not found")

    # récupérer le nom du backup à partir du tag
    backup_name = getFileNameByTag(connection, tag, project_name)

    # vérifie que le backup_name existe dans le projet
    try:
        connection.run(f"find ./kdna/{project_name}/{backup_name}")
    except Exception:
        raise Exception(f"Tag {tag} not found in project {project_name}")
    # renvoie le path du backup
    return f"./kdna/{project_name}/{backup_name}"
