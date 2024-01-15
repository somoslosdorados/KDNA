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
from kdna.parsing.parser import listServers
from kdna.encrypt import encrypt
from kdna.parsing.parser import kdna_path
from kdna.ssh.ssh_client import SSHClient
from kdna.server.server import upload_file, download_file, find_path
from kdna.read_backups.agent import list_backups
from kdna.logger import logger

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
@click.option('--prefix', required=False, help="generate an unique tag", type=bool)
def add(project, path, tag, prefix=None):
    """
    Commande pour sauvegarder un fichier ou un dossier.\n
    Arguments obligatoires :\n
    \t- <project>: le nom du projet à sauvegarder\n
    \t- <path>: le chemin du dossier ou fichier à sauvegarder\n
    \t- <tag>: le tag de la sauvegarde

    author: Baptiste BRONSIN
    """

    if len(listServers) == 0:
        click.echo("Any server found in the configuration file.")
        return

    if not os.path.exists(path):
        click.echo("Directory '" + path + "' is missing.")
        return

    uuid_backup = str(uuid.uuid4())
    name_of_temp_backup = encrypt.package(
        path, uuid_backup, kdna_path, listServers[0].encrypt)
    path_to_local_backup = os.path.join(kdna_path, name_of_temp_backup)
    path_to_remote_backup = os.path.join("~/kdna", project)
    serversCredential = listServers[0].credentials

    try:
        instance = SSHClient(serversCredential).connect()
    except PermissionError as exc:
        click.echo("Création d'une connexion SSH : vous n'avez pas les droits")
        logger.log("ERROR", "Erreur lors de l'instanciation d'une connexion SSH, il s'agit d'un problème de droits")
        return
    except Exception as e:
        print("Création d'une connexion SSH : error2 = " + e.__str__())
        logger.log("ERROR", "Erreur lors de l'instanciation d'une connexion SSH")
        return
    
    try:
        if prefix is not None:
            tag = tags.generate_tag_name(instance.connection, project, tag)
            logger.log("INFO", "Un tag unique a été généré avec le préfixe : " + tag)
    except PermissionError as exc:
        click.echo("Génération du tag préfixé : vous n'avez pas les droits")
        logger.log("ERROR", "Erreur lors de la création d'un tag unique, il s'agit d'un problème de droits")
        return
    except Exception as e:
        click.echo("Génération du tag préfixé : error" + e.__str__())
        logger.log("ERROR", "Erreur lors de la création d'un tag unique")
        return

    click.echo(f"Creating backup in {project} with {tag} tag")

    try:
        upload_file(instance.connection, path_to_local_backup, path_to_remote_backup)
        logger.log("INFO", "La backup a été uploadée sur le serveur distant")
    except FileNotFoundError as exc:
        click.echo("Envoi du fichier sur le serveur : le fichier n'a pas été trouvé")
        logger.log("ERROR", "Erreur lors de l'upload de la backup sur le serveur distant, le fichier n'a pas été trouvé")
        return
    except PermissionError as exc:
        click.echo("Envoi du fichier sur le serveur : vous n'avez pas les droits")
        logger.log("ERROR", "Erreur lors de l'upload de la backup sur le serveur distant, il s'agit d'un problème de droits")
        return
    except Exception as e:
        click.echo("Envoi du fichier sur le serveur : error = " + e.__str__())
        logger.log("ERROR", "Erreur lors de l'upload de la backup sur le serveur distant")
        return

    try:
        os.remove(path_to_local_backup)
        logger.log("INFO", "La backup locale a été supprimée à '" + path_to_local_backup + "'")
    except FileNotFoundError as exc:
        click.echo("Suppression de la buckup locale : le fichier n'a pas été trouvé")
        logger.log("ERROR", "Erreur lors de la suppression de la backup locale à '" + path_to_local_backup + "', le fichier n'a pas été trouvé")
        return
    except PermissionError as exc:
        click.echo("Suppression de la buckup locale : vous n'avez pas les droits")
        logger.log("ERROR", "Erreur lors de la suppression de la backup locale à '" + path_to_local_backup + "', il s'agit d'un problème de droits")
        return
    except Exception as e:
        click.echo("Suppression de la buckup locale : error = " + e.__str__())
        logger.log("ERROR", "Erreur lors de la suppression de la backup locale à '" + path_to_local_backup + "'")
        return

    try:
        tags.add_tags(instance.connection, project, tag, name_of_temp_backup)
    except PermissionError as exc:
        click.echo("Ajout du tag sur la backup : vous n'avez pas les droits")
        return
    except Exception as e:
        click.echo("Ajout du tag sur la backup : error" + e.__str__())
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
    \t- <project_name>: le nom du projet pour lequel lister les backups
    
    author: Baptiste BRONSIN
    """

    if len(listServers) == 0:
        click.echo("Any server found in the configuration file.")
        return

    try:
        instance = SSHClient(listServers[0].credentials).connect()
    except Exception as e:
        print("error = "+e.__str__())

    backups = []

    try:
        backups = list_backups(instance.connection, project_name)
        dic = tags.get_tag_conf(instance.connection, project_name)
        for key in dic.keys():
            click.echo(f"Backup : {dic[key]} - Tag : {key}")

    except Exception as e:
        print("error2 = "+e.__str__())

    if backups is None:
        click.echo(f'Project {project_name} not found')
    # else:
        # click.echo('Backups : ' + str(backup


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

    try:
        instance = SSHClient(listServers[0].credentials).connect()
    except Exception as e:
        print(e)

    remote_path = find_path(instance.connection, nametag, project)

    local_temp_path = os.path.join(
        kdna_path, "temp", remote_path.split("/")[-1])

    try:
        download_file(instance.connection, local_temp_path, remote_path)
    except Exception as e:
        print(e)

    try:
        restored_path= encrypt.restore(local_temp_path, path)
    except Exception as e:
        print(e)

    click.echo(f"Restauration faite : \"{restored_path}\"")
    os.remove(local_temp_path)
