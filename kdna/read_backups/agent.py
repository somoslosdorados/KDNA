from fabric import Connection
from kdna.logger.logger import log  # type: ignore
from kdna.server.server import directory_exists


def list_projects(connection: Connection) -> list | None:
    """
    Retourne tous les projets.

    Arguments: connection (fabric.Connection)
    """
    try:
        result = connection.run("ls -l kdna/ | grep '^d'", hide=True)

        return ["".join((":".join(line.split(':')[1:]))[3:]) for line in
                result.stdout.split('\n')[:-1]]
    except:
        print("Une erreur est survenue lors de la récupération des projets")
        log("ERROR", "An error as occured when getting projects")
        return None


def list_backups(connection: Connection, project_name: str) -> list | None:
    """
    Retourne toutes les backups pour un projet donné.

    Arguments: connection (fabric.Connection), project_name (str)
    """
    try:
        if not directory_exists(connection, "kdna/" + project_name):
            print("The directory 'kdna/" + project_name + "' doesn't exist.")
            log("ERROR", "The directory 'kdna/" + project_name + "' doesn't exist.")
            return None

        result = connection.run(
            f"ls -l kdna/{project_name} | grep '^\-'", hide=True)

        backups = []
        for line in result.stdout.split('\n')[:-1]:
            file_name = "".join((":".join(line.split(':')[1:]))[3:])

            if file_name != "tags.conf":
                backups.append(file_name)

        return backups
    except Exception as e:
        print("An error as occured when getting backups")
        log("ERROR", "An error as occured when getting backups" + e)
        return None
