"""
Groupe de commandes auto-backup qui permet de gérer les backups
add : Commande pour créer une backup
delete : Commande pour supprimer une backup
update : Commande pour mettre à jour une backup
restore : commande pour restaurer une backup
list : Commande pour lister les backups
"""

import click
import uuid
import os
import kdna.tags.tags as tags
from kdna.logger import logger
from kdna.parsing.parser import listServers
from kdna.encrypt import encrypt
from kdna.parsing.parser import kdna_path
from kdna.ssh.ssh_client import SSHClient
from kdna.server.server import upload_file, download_file, find_path
from kdna.read_backups.agent import list_backups

# Creation du groupe de commande backup


@click.group()
def backup():
    """Commande pour sauvegarder un fichier ou un dossier"""


# Création des commandes du groupe backup

# Création de la commande add
@backup.command()
@click.argument('project', nargs=1, required=True)
@click.argument('path', nargs=1, required=True)
@click.argument('tag', nargs=1, required=True)
def add(project, path, tag):
    """
    Commande pour sauvegarder un fichier ou un dossier.\n
    Arguments obligatoires :\n
    \t- <project>: le nom du projet à sauvegarder\n
    \t- <path>: le chemin du dossier ou fichier à sauvegarder\n
    \t- <tag>: le tag de la sauvegarde

    author: Baptiste BRONSIN
    """

    click.echo(f"Création de la backup dans {project} avec le tag {tag}")
    logger.log("INFO", f"Création de la backup dans {project} avec le tag {tag}")

    if len(listServers) == 0:
        click.echo("Pas de serveur trouvé dans le fichier de configuration.")
        logger.log("ERROR", "Pas de serveur trouvé dans le fichier de configuration.")
        return

    if not os.path.exists(path):
        click.echo("Le dossier '" + path + "' n'existe pas.")
        logger.log("ERROR", "Le dossier '" + path + "' n'existe pas.")
        return

    uuid_backup = str(uuid.uuid4())
    name_of_temp_backup = encrypt.package(path, uuid_backup, kdna_path, listServers[0].encrypt)
    path_to_local_backup = os.path.join(kdna_path, name_of_temp_backup)
    path_to_remote_backup = os.path.join("kdna", project)
    serversCredential = listServers[0].credentials

    try:
        instance = SSHClient(serversCredential).connect()
    except PermissionError as exc:
        click.echo("Création d'une connexion SSH : vous n'avez pas les droits")
        logger.log("ERROR", "Création d'une connexion SSH : vous n'avez pas les droits")
        return
    except Exception as e:
        click.echo("Création d'une connexion SSH : error2 = " + e.__str__())
        logger.log("ERROR", "Création d'une connexion SSH : error2 = " + e.__str__())
        return

    try:
        upload_file(instance.connection, path_to_local_backup, path_to_remote_backup)
    except FileNotFoundError as exc:
        click.echo("Envoi du fichier sur le serveur : le fichier n'a pas été trouvé")
        logger.log("ERROR", "Envoi du fichier sur le serveur : le fichier n'a pas été trouvé")
        return
    except PermissionError as exc:
        click.echo("Envoi du fichier sur le serveur : vous n'avez pas les droits")
        logger.log("ERROR", "Envoi du fichier sur le serveur : vous n'avez pas les droits")
        return
    except Exception as e:
        click.echo("Envoi du fichier sur le serveur : error = " + e.__str__())
        logger.log("ERROR", "Envoi du fichier sur le serveur : error = " + e.__str__())
        return

    try:
        os.remove(path_to_local_backup)
    except FileNotFoundError as exc:
        click.echo("Suppression de la backup locale : le fichier n'a pas été trouvé")
        logger.log("ERROR", "Suppression de la backup locale : le fichier n'a pas été trouvé")
        return
    except PermissionError as exc:
        click.echo("Suppression de la backup locale : vous n'avez pas les droits")
        logger.log("ERROR", "Suppression de la backup locale : vous n'avez pas les droits")
        return
    except Exception as e:
        click.echo("Suppression de la backup locale : error = " + e.__str__())
        logger.log("ERROR", "Suppression de la backup locale : error = " + e.__str__())
        return

    try:
        tags.add_tags(instance.connection, project, tag, name_of_temp_backup)
    except PermissionError as exc:
        click.echo("Ajout du tag sur la backup : vous n'avez pas les droits")
        logger.log("ERROR", "Ajout du tag sur la backup : vous n'avez pas les droits")
        return
    except Exception as e:
        click.echo("Ajout du tag sur la backup : error" + e.__str__())
        logger.log("ERROR", "Ajout du tag sur la backup : error" + e.__str__())
        return

# Création de la commande delete
@backup.command()
@click.option('-t', 'pathtag', nargs=1, required=True, help="entrer le path du fichier et le tag [ path:tag ]")
def delete(pathtag):
    """Commande pour supprimer une backup.\n"""
    click.echo(f"Suppression du fichier : \"{pathtag}\"")


# Création de la commande list
@backup.command()
@click.argument('project_name', nargs=1, required=True)
def list(project_name):
    """Commande pour lister les backups d'un projet\n
    Argument obligatoire :\n
    \t- <project_name>: le nom du projet pour lequel lister les backups"""

    if len(listServers) == 0:
        click.echo("Pas de serveur trouvé dans le fichier de configuration.")
        logger.log("ERROR", "Pas de serveur trouvé dans le fichier de configuration.")
        return

    try:
        instance = SSHClient(listServers[0].credentials).connect()
    except Exception as e:
        click.echo("Erreur lors de la récupération des backups = "+e.__str__())
        logger.log("ERROR", "Erreur lors de la récupération des backups = "+e.__str__())

    backups = []

    try:
        backups = list_backups(instance.connection, project_name)
        dic = tags.get_tag_conf(instance.connection, project_name)
        for key in dic.keys():
            click.echo(f"Backup : {dic[key]} - Tag : {key}")

    except Exception as e:
        print("error2 = "+e.__str__())

    if backups is None:
        click.echo(f'Projet {project_name} non trouvé')
        logger.log("ERROR", f'Projet {project_name} non trouvé')
    # else:
        # click.echo('Backups : ' + str(backups))
        # click.echo('Tags : ' + str(backups))


# Création de la commande restore
@backup.command()
@click.option('-p', '--project', nargs=1, required=True,
              help="entrer le nom du projet à restaurer")
@click.option('-t', '--nametag', nargs=1, required=True,
              help="entrer le nom du fichier à restaurer et le tag [ name:tag ]")
@click.argument('path', nargs=1, required=True)
def restore(project, nametag, path):
    """Commande pour restaurer une backup.\n
        Argument obligatoire :\n
        \t- <path>: le chemin du fichier ou du dossier à restaurer\n"""
    click.echo(f"Restauration du fichier : \"{nametag}\"")

    if len(listServers) == 0:
        click.echo("Pas de serveur trouvé dans le fichier de configuration.")
        logger.log("ERROR", "Pas de serveur trouvé dans le fichier de configuration.")
        return

    try:
        instance = SSHClient(listServers[0].credentials).connect()
    except Exception as e:
        click.echo("Erreur lors de la connexion au serveur : "+e.__str__())
        logger.log("ERROR", "Erreur lors de la connexion au serveur : "+e.__str__())

    remote_path = find_path(instance.connection, nametag, project)

    local_temp_path = os.path.join(
        kdna_path, "temp", remote_path.split("/")[-1])

    try:
        download_file(instance.connection, local_temp_path, remote_path)
    except Exception as e:
        click.echo("Erreur lors du téléchargement du fichier : "+e.__str__() + " " + remote_path)
        logger.log("ERROR", "Erreur lors du téléchargement du fichier : "+e.__str__() + " " + remote_path)

    try:
        restored_path = encrypt.restore(local_temp_path, path)
    except Exception as e:
        click.echo("Erreur lors de la restauration du fichier : "+e.__str__())
        logger.log("ERROR", "Erreur lors de la restauration du fichier : "+e.__str__())

    click.echo(f"Restauration faite : \"{restored_path}\"")
    logger.log("INFO", f"Restauration faite : \"{restored_path}\"")
    os.remove(local_temp_path)
