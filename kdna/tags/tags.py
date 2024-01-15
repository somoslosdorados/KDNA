"""We will use connexion instance gathered by the module
    If the service is running the tags.conf file could change
    
    authors: Dorian TETU, Hugo PONTHIEU"""

import time
from fabric import Connection
from kdna.logger import logger


def backup_exist(connection_instance: Connection, project: str, file_to_tag: str) -> bool:
    """
    Check if a backup file exists on the server.

    :param connection_instance: An instance of the Connection class representing the server
    connection.
    :type connection_instance: Connection

    :param project: The name of the project.
    :type project: str

    :param file_to_tag: The name of the file to check for existence.
    :type file_to_tag: str

    :return: True if the backup file exists, False otherwise.
    :rtype: bool
    """
    # Vérification que la sauvegarde existe sur le serveur
    try:
        connection_instance.run(
            f"ls ./kdna/{project}/{file_to_tag}", hide=True)
    except Exception as e:
        logger.log(
            "ERROR", f"Erreur lors de la vérification de l'existence de {file_to_tag}"
                     f" pour le project {project}: {e}")
        return False
    return True


def add_tags(connection_instance: Connection, project: str, new_tag: str, file_to_tag: str):
    """arguments: ssh instance / name of the project / name of the tags
    In the file tag.conf we must identify the tag [tags] to write tags at the end 
    of the file

    authors: Dorian TETU, Hugo PONTHIEU"""
    # VERIFIER QUE LES TAGS NE SONT PAS EXISTANT !!!!!!!!!!!!!
    # Vérification que la backup existe sur le serveur
    if not backup_exist(connection_instance, project, file_to_tag):
        logger.log(
            "ERROR", f"Erreur lors de l'ajout de {new_tag} pour le project {project}"
                     f", {file_to_tag} n'existe pas")
        raise FileNotFoundError("Erreur: le fichier n'existe pas")
    if (tag_exists(connection_instance, project, new_tag)):
        logger.log(
            "ERROR", f"Erreur lors de l'ajout de {new_tag} pour le project {project},"
                     f" {new_tag} existe déjà")
        raise KeyError(f"{new_tag} existe déjà")

    dico = get_tag_conf(connection_instance, project)
    # Ecrire dans le fichier tag.conf le nouveau tag
    dico[new_tag] = file_to_tag
    write_tag_conf(connection_instance, project, dico)
    logger.log(
        "INFO", f"Le tag {new_tag} a été ajouté au fichier {file_to_tag} du projet"
                f" {project}")


def delete_tags(connection_instance: Connection, project: str, old_tag: str):
    """arguments: oldTag """
    # Récupération du fichier tag.conf
    tag_file = get_tag_conf(connection_instance, project)

    # Verification de la présence du tag
    if (not tag_exists(connection_instance, project, old_tag)):
        logger.log(
            "ERROR", f"Erreur lors de la suppression de {old_tag} pour le project"
                     f" {project}, {old_tag} n'existe pas")
        raise KeyError(f"{old_tag} n'existe pas")
    # Deletion de du tag à enlever
    tag_file.pop(old_tag)
    # Ecriture dans le fichier
    write_tag_conf(connection_instance, project, tag_file)
    logger.log("INFO", f"Le tag {old_tag} a été supprimé du projet {project}")


def update_tags(connection_instance: Connection, project: str, old_tag: str, new_tag: str):
    """
    Update the tags in the tag configuration file for a specific project.

    :param connection_instance: The connection instance to use for the update.
    :type connection_instance: Connection
    :param project: The name of the project.
    :type project: str
    :param old_tag: The old tag to be updated.
    :type old_tag: str
    :param new_tag: The new tag to replace the old tag.
    :type new_tag: str
    :raises KeyError: If the old tag does not exist or if the new tag already exists.
    """
    tag_file = get_tag_conf(connection_instance, project)
    file_to_tag = tag_file[old_tag]
    if not tag_exists(connection_instance, project, old_tag):
        logger.log(
            "ERROR", f"Erreur lors de l'update de {old_tag} en {new_tag} pour le"
                     f" project {project}, {old_tag} n'existe pas")
        raise KeyError(f"{old_tag} n'existe pas")

    if tag_exists(connection_instance, project, new_tag):
        logger.log(
            "ERROR", f"Erreur lors de l'update de {old_tag} en {new_tag} pour le"
                     f" project {project}, {new_tag} existe déjà")
        raise KeyError(f"{new_tag} existe déjà")

    tag_file.pop(old_tag)
    tag_file[new_tag] = file_to_tag

    write_tag_conf(connection_instance, project, tag_file)
    logger.log(
        "INFO", f"Le tag {old_tag} a été modifié en {new_tag} dans le projet"
                f" {project}")


def get_file_name_by_tag(connection_instance: Connection, project: str, tag: str) -> str:
    """
    Retrieves the file name associated with a given tag in a specific project.

    Args:
        connection_instance (Connection): An instance of the Connection class.
        project (str): The name of the project.
        tag (str): The tag to search for.

    Returns:
        str: The file name associated with the given tag.

    Raises:
        FileNotFoundError: If no file is associated with the given tag in the project.

    """
    dico = get_tag_conf(connection_instance, project)
    if tag in dico:
        return dico[tag]
    # Si aucun fichier n'est trouvé une erreur apparait
    logger.log(
        "ERROR", f"Aucun fichier n'a été associé au tag {tag} dans le project"
                 f" {project}")
    raise FileNotFoundError(
        f"Aucun fichier n'a été associé au tag {tag} dans le project {project}")


def check_init_tag_file(connection_instance: Connection, project: str):
    """
    Check if the tags.conf file exists in the specified project directory.
    If the file does not exist, it will be created.

    :param connection_instance: An instance of the Connection class.
    :type connection_instance: Connection
    :param project: The name of the project.
    :type project: str
    """
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    try:
        connection_instance.run(f"find {path_to_conf_tag}", hide=True)
    except Exception as e:
        logger.log(
            "INFO", f"Le fichier {path_to_conf_tag} n'existe pas, il va être créé")
        connection_instance.run(
            f"echo '[tags]' > {path_to_conf_tag}", hide=True)


def tag_exists(connection_instance: Connection, project: str, tag: str) -> bool:
    """Check if the tag exists in the project"""
    dico = get_tag_conf(connection_instance, project)
    if tag in dico:
        return True
    return False


def generate_tag_name(connection_instance: Connection, project: str, prefix: str) -> str:
    """
    Generates a unique tag name by appending a timestamp to the given prefix.

    :param connection_instance: An instance of the Connection class representing the connection to
     the database.
    :type connection_instance: Connection
    :param project: The name of the project.
    :type project: str
    :param prefix: The prefix to be used in the generated tag name.
    :type prefix: str
    :return: The generated unique tag name.
    :rtype: str
    """
    ct = time.time()
    new_tag = prefix + "_" + str(ct)
    new_tag_decorated = new_tag

    # check if the tag exists
    if tag_exists(connection_instance, project, new_tag):
        found = False
        while not found:
            # increment the tag, exemple: tag_1, tag_2, tag_3
            ct += 1
            new_tag_decorated = new_tag + "_" + ct
            if not tag_exists(connection_instance, project, new_tag_decorated):
                found = True
    logger.log("INFO", f"Le tag {new_tag_decorated} a été généré")
    return new_tag_decorated


def get_tag_conf(connection_instance: Connection, project: str) -> dict:
    """Get the tag.conf file and return a dictionnary with the tags, exemple: {"tag1": "file1",
     "tag2": "file2"}"""
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    check_init_tag_file(connection_instance, project)
    result = connection_instance.run(f"cat {path_to_conf_tag}", hide=True)
    resultset = result.stdout.splitlines()
    resultset.pop(0)
    dictionnaire = {}
    for line in resultset:
        if line != "":
            dictionnaire[line.split(", ")[0]] = line.split(", ")[1]
    return dictionnaire


def write_tag_conf(connection_instance: Connection, project: str, dictionnaire: dict):
    """Write the dictionnary in the tag.conf file"""
    path_to_conf_tag = "./kdna/"+project+"/tags.conf"
    texte_conf = "[tags]\n"
    for key in dictionnaire:
        texte_conf += key + ", " + dictionnaire[key] + "\n"
    try:
        connection_instance.run(
            f"echo \"{texte_conf}\" > {path_to_conf_tag}", hide=True)
    except Exception as e:
        logger.log(
            "ERROR", f"Erreur inconnue lors de l'écriture dans tags.conf: {e}")
        raise Exception("Erreur inconnue lors de l'écriture dans tags.conf")
