"""
Groupe de commandes server qui permet de gérer les serveurs (backups régulières)
add: Commande pour ajouter un serveur au fichier de configuration
delete : Commande pour supprimer un serveur du fichier de configuration
update : Commande pour mettre à jour un serveur
list : Commande pour lister les serveurs
"""

import click
from kdna.logger.logger import log
from kdna.server.server_service import ServerService
from tabulate import tabulate
from kdna.ssh.ssh_client import SSHClient
from kdna.conf_utils.utils import Utils


@click.group()
def server():
    """Commande pour gérer les serveurs"""


#! Création des commandes du groupe server


# Création de la commande init
@server.command()
def init():
    """Commande pour initialiser le fichier de configuration"""
    Utils.initialize_config_file()


# Création de la commande add
@server.command()
@click.option("-i", "--id", default="", required=False, help="entrer l'id Ex: 1")
@click.option(
    "-ad",
    "--address",
    required=True,
    help="entrer le libelé de connexion " "Ex: user@host",
)
@click.option("-a", "--alias", required=True, help="entrer l'alias Ex: serveur1")
@click.option(
    "-r",
    "--repo",
    required=True,
    help="entrer le répertoire de sauvegarde " "Ex: /home/user/backup",
)
@click.option(
    "-p",
    "--port",
    default=22,
    required=False,
    help="entrer le port (valeur par defaut : 22)",
)
@click.option(
    "-e",
    "--encrypt",
    default=True,
    required=False,
    help="Encrypt les "
    "sauvegardes sur le serveur (valeur par defaut : True) Ex: False",
)
def add(id, alias, address, repo, port, encrypt):
    """Commande pour ajouter un serveur."""
    try:
        server_service = ServerService()
        server_service.create_server(id, address, repo, port, encrypt, alias)
    except Exception:
        print("An error occurred while connecting to this address.")
        log("ERROR", "An error occurred while connecting to this address.")
        return None


# Création de la commande delete
@server.command()
@click.option(
    "-a", "--alias", required=False, help="entrer l'alias du serveur à supprimer"
)
@click.option("-i", "--id", required=False, help="entrer l'id du serveur à supprimer")
def delete(alias, id):
    """Commande pour supprimer un serveur."""
    serverService = ServerService()
    if alias:
        serverService.delete_server(alias, True)
    else:
        if id:
            serverService.delete_server(id)
        else:
            click.echo("L'argument alias ou id doit être renseigné.")


# Création de la commande update
@server.command()
@click.argument("alias", required=True)
@click.option(
    "-r",
    "--new_repo",
    default="",
    required=False,
    help="entrer le répertoire" " de sauvegarde Ex: /home/user/backup",
)
@click.option("-p", "port", default="", required=False, help="entrer le nouveau port")
@click.option(
    "-ad",
    "new_address",
    default="",
    required=False,
    help="entrer la nouvelle" " adresse",
)
@click.option(
    "-a", "new_alias", default="", required=False, help="entrer le nouvel" " alias"
)
@click.option(
    "-e",
    "--encrypt",
    default="",
    required=False,
    help="Encrypt les "
    "sauvegardes sur le serveur (valeur par defaut : True) Ex: False",
)
def update(alias, new_repo, port, new_address, encrypt, new_alias):
    """
    Commande pour mettre à jour un serveur.\n
    argument obligatoire :\n
    \t- <alias>: l'alias du serveur à mettre à jour
    """
    serverService = ServerService()
    if (
        alias
        and new_address
        or alias
        and new_repo
        or alias
        and port
        or alias
        and encrypt
        or alias
        and new_alias
    ):
        serverService.update_server(
            alias, new_repo, port, new_address, encrypt, new_alias
        )
    else:
        click.echo("Les arguments à mettre à jour doivent être renseignés.")


# Création de la commande list


@server.command()
def list():
    """Commande pour lister les serveurs"""
    serverService = ServerService()
    servers = serverService.find_all()
    table = tabulate(
        [[data for data in server.values()] for server in servers],
        ["id", "host", "path", "port", "encrypt", "alias"],
        tablefmt="grid",
    )
    click.echo(table)


@server.command()
@click.argument("alias", required=True)
def status(alias):
    """Commande pour afficher le statut d'un serveur"""
    serverService = ServerService()
    server = serverService.find_by_alias(alias)
    click.echo(server.get_status())


@server.command()
def ssh_import():
    """Import server from ~/.ssh/config file"""
    serverService = ServerService()
    serverService.import_server()
