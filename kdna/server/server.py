from fabric import Connection
from kdna.tags.tags import getFileNameByTag

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

# méthode pour trouver le path d'un backup à partir d'un tag et d'un nom de projet
def find_path(connection: Connection, tag: str, project_name: str) -> str:
    """
    Find a path in the remote server. Might throw an exception.
    """

    # vérifier que le dossier du projet existe
    try:
        connection.run(f"ls ./kdna/{project_name}") 
    except:
        raise Exception(f"Project {project_name} not found")
    
    # récupérer le nom du backup à partir du tag
    backup_name = getFileNameByTag(connection, tag, project_name)
     
     # vérifie que le backup_name existe dans le projet
    try:
        connection.run(f"find ./kdna/{project_name}/{backup_name}")
    except:
        raise Exception(f"Tag {tag} not found in project {project_name}")
    
    
    # renvoie le path du backup
    return f"./kdna/{project_name}/{backup_name}"


def main ():
    with Connection("test@192.168.122.226") as c:
       print( getFileNameByTag(c,'project1','a'))

if __name__ == '__main__':
    main()