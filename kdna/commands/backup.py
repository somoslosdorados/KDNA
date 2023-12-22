import click
import os
import kdna.tags.tags as tags
from kdna.parsing.parser import listServers
from kdna.encrypt.encrypt import package
from kdna.parsing.parser import kdna_path
from kdna.ssh.ssh_client import SSHClient
from kdna.server.server import upload_file, download_file

# Creation du groupe de commande backup


@click.group()
def backup():
    """Commande pour sauvegarder un fichier"""


# Création de la fonction display pour afficher le contenu d'un fichier
def display(path):
    """Fonction pour afficher le contenu d'un fichier\n
    :param path: le path du fichier à afficher\n
    :type path: str\n
    :return: le contenu du fichier\n
    :rtype: str"""
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Fichier non trouvé") from exc

    except PermissionError as exc:
        raise PermissionError("Oups, Pas les droits") from exc


# Création des commandes du groupe backup

# Création de la commande add
@backup.command()
@click.argument('name', nargs=1, required=True)
@click.argument('path', nargs=1, required=True)
@click.argument('tag', nargs=1, required=True)
def add(name, path, tag):
    """Commande pour sauvegarder un fichier\n
    :param name: le nom du fichier à sauvegarder\n
    :type name: str\n
    :param path: le path du fichier à sauvegarder\n
    :type path: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    click.echo(f"Creating backup \"{name}\":\n{tag}")
    name_of_temp_backup = package(path, name, kdna_path, True)
    path_to_local_backup = os.path.join(kdna_path, name_of_temp_backup)
    path_to_remote_backup = os.path.join("kdna", "project")
    serversCredential = listServers[0].credentials
    try:
        instance = SSHClient(serversCredential).connect()
    except Exception as e:
        print("error2 = "+e.__str__())

    try:
        upload_file(instance.connection, path_to_local_backup,
                    path_to_remote_backup)
        os.remove(path_to_local_backup)
        tags.addTags(instance.connection, "project",
                     tag, name_of_temp_backup, True)
    except Exception as e:
        print("error = "+e.__str__())

# Création de la commande delete


@backup.command()
@click.option('-t', 'pathtag', nargs=1, required=True, help="entrer le path du fichier et le tag [ path:tag ]")
def delete(pathtag):
    """Commande pour supprimer un fichier\n
    :param pathtag: -t [ path:tag ] le path du fichier à supprimer et le tag\n
    :type pathtag: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    click.echo(f"Suppression du fichier : \"{pathtag}\"")


# Création de la commande list
@backup.command()
def list():
    """Commande pour lister les fichiers sauvegardés
    :return: Liste des fichiers sauvegardés : class: `str`\n
    :rtype: list"""
    click.echo(f"List of backup : \n...\n...")


# Création de la commande restore
@backup.command()
@click.option('-t', '--nametag', nargs=1, required=True,
              help="entrer le nom du fichier à restaurer et le tag [ name:tag ]")
@click.argument('path', nargs=1, required=True)
def restore(nametag, path):
    """Commande pour restaurer un fichier\n
    :param nametag: -t [ name:tag ] le nom du fichier à restaurer
    :type nametag: str\n
    :param path: le path du fichier à restaurer\n
    :type path: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    click.echo(f"Restauration du fichier : \"{nametag}\"")
    try:
        instance = SSHClient(listServers[0].credentials).connect()
    except Exception as e:
        print(e)

    remote_path = os.path.join("kdna", "project", nametag.split(":")[0])
    local_temp_path = os.path.join(kdna_path, "temp", nametag.split(":")[0])

    try:
        download_file(instance.connection, path, remote_path)
