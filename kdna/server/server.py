# mypy: ignore-errors
from fabric import Connection
from kdna.logger.logger import log  # type: ignore
from kdna.ssh.ssh_client import SSHClient
from kdna.tags.tags import get_file_name_by_tag


class Server:
    """
    A class representing a server.

    :param creds: The credentials required to establish a connection to the server.
    :type creds: dict
    """
    def __init__(self, creds):
        self.client: SSHClient = SSHClient(creds)
        self.client.connect()
        self.creds = creds

    def directory_exists(self, path: str) -> bool:
        """
        Check if a directory exists at the given path.

        :param path: A string representing the path to the directory.
        :type path: str
        :return: True if the directory exists, False otherwise.
        :rtype: bool
        """
        return self.client.connection.run(f"test -d {path}", warn=True).ok

    def upload_file(self, local_path: str, remote_path: str):
        """
        Uploads a file from the local machine to the remote server.

        :param local_path: The path of the file on the local machine.
        :type local_path: str
        :param remote_path: The path where the file will be uploaded on the remote server.
        :type remote_path: str
        """
        if not self.directory_exists(remote_path):
            self.client.connection.run(f"mkdir -p {remote_path}")
        self.client.connection.put(local_path, remote=remote_path)

    def get_status(self):
        """
        Returns the status of the client.

        :return: The status of the client.
        :rtype: str
        """
        return self.client.status()

    def download_file(self, local_path: str, remote_path: str):
        """
        Downloads a file from a remote path to a local path.

        :param local_path: The local path where the file will be downloaded to.
        :type local_path: str
        :param remote_path: The remote path from where the file will be downloaded.
        :type remote_path: str
        :raises Exception: If no file is found on the remote path.
        """
        files = self.client.connection.run(f"mkdir -p {remote_path}", warn=True).stdout.split("\n")
        if len(files) == 0:
            log("ERROR", "Error: no file found on " + remote_path)
            raise Exception(f"Error: no file found on {remote_path}")
        for file in files:
            self.client.connection.get(file, local=local_path)


def directory_exists(connection: Connection, path: str):
    """
    Check if a directory exists on the remote server. Might throw an exception.
    """
    t = connection.run(f"test -d {path}", warn=True).ok
    print(t)
    log("INFO", "directory_exists: " + str(t))
    return t


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
    files = connection.run(f"ls {remote_path}", warn=True).stdout.split("\n")
    if len(files) == 0:
        log("ERROR", "Error: no file found on : " + remote_path)
        raise Exception(f"Error: no file found on {remote_path}")
    for file in files:
        connection.get(file, local=local_path)



# méthode pour trouver le path d'un backup à partir d'un tag et d'un nom de projet


def find_path(connection: Connection, tag: str, project_name: str) -> str:
    """
    Find a path in the remote server. Might throw an exception.
    """
    log("INFO", "find_path: tag= " + tag + " project_name= " + project_name)
    print(f"find_path: tag={tag}, project_name={project_name}")

    # vérifier que le dossier du projet existe
    try:
        connection.run(f"ls ./kdna/{project_name}")
    except Exception:
        log("ERROR", "Project " + project_name + "not found")
        raise Exception(f"Project {project_name} not found")

    # récupérer le nom du backup à partir du tag
    backup_name = get_file_name_by_tag(
        connection, project_name, tag).removesuffix("\n")

    # vérifie que le backup_name existe dans le projet
    try:
        connection.run(f"find ./kdna/{project_name}/{backup_name}")
    except Exception:
        log("ERROR", "Tag " + tag + "not found in project " + project_name)
        raise Exception(f"Tag {tag} not found in project {project_name}")
    # renvoie le path du backup
    return f"./kdna/{project_name}/{backup_name}"


def find_all_file(connection: Connection, tag: str, verbose=False) -> list:
    """return a list of path of backups that or tag with the given tag"""
    # Listing des différents projets
    # Listing des différents projets
    try:
        projects = connection.run("ls ./kdna/", hide=True).stdout
    except:
        log("ERROR", "Can't list projects")
        raise Exception("Can't list projects")
    # Trier la liste
    listedProject = list(filter(lambda item: item != "", projects.split("\n")))
    paths_list = []
    message = "Vos sauvegardes: \n"
    # Vérifie dans chaque project si il existe une backup associé au tag
    for project in listedProject:
        try:
            fileName = get_file_name_by_tag(
                connection, project, tag).strip("\n")
            paths_list.append(f"/{project}/{fileName}")
            message += 'In {:>8}:{:>8}{:>8}\n'.format(project, tag, fileName)
        except Exception:
            message += f"No file tagged {tag} in {project}\n"

    if (verbose):
        print(" verbose : " + message)
        log("INFO", "verbose : " + message)
    return paths_list
