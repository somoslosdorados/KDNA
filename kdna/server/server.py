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
    files = connection.run(f"ls {remote_path}", warn=True).stdout.split("\n")
    if len(files) == 0:
        raise Exception(f"Error: no file found on {remote_path}")
    for file in files:
        connection.get(file, local=local_path)

# méthode pour trouver le path d'un backup à partir d'un tag et d'un nom de projet


def find_path(connection: Connection, tag: str, project_name: str) -> str:
    """
    Find a path in the remote server. Might throw an exception.
    """
    print(f"find_path: tag={tag}, project_name={project_name}")

    # vérifier que le dossier du projet existe
    try:
        connection.run(f"ls ./kdna/{project_name}")
    except Exception:
        raise Exception(f"Project {project_name} not found")

    # récupérer le nom du backup à partir du tag
    backup_name = getFileNameByTag(
        connection, project_name, tag).removesuffix("\n")

    # vérifie que le backup_name existe dans le projet
    try:
        connection.run(f"find ./kdna/{project_name}/{backup_name}")
    except Exception:
        raise Exception(f"Tag {tag} not found in project {project_name}")
    # renvoie le path du backup
    return f"./kdna/{project_name}/{backup_name}"

def find_all_file(connection: Connection, tag: str,verbose=False):
    """return a list of path of backups that or tag with the given tag"""
     #Listing des différents projets
    try:
        projects=connection.run(f"ls ./kdna/",hide=True).stdout
    except:
        raise Exception("Can't list projects")
    #Trier la liste
    listedProject=list(filter(lambda item:item!="",projects.split("\n")))
    paths_list=[]
    message="Vos sauvegardes: \n"
    #Vérifie dans chaque project si il existe une backup associé au tag
    for project in listedProject:
        try:
            fileName=getFileNameByTag(connection, project, tag).strip("\n")
            paths_list.append(f"/{project}/{fileName}")
            message+='In {:>8}:{:>8}{:>8}\n'.format(project,tag,fileName)
        except:
            message+=f"No file tagged {tag} in {project}\n"
    
    if(verbose):
        print(message)
    return paths_list
