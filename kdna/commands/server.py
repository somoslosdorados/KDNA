"""
Groupe de commandes server qui permet de gérer les serveurs (backups régulières)
add: Commande pour ajouter un serveur au fichier de configuration
delete : Commande pour supprimer un serveur du fichier de configuration
update : Commande pour mettre à jour un serveur
list : Commande pour lister les serveurs
"""

import click
from kdna.server.server_service import ServerService
from tabulate import tabulate
from kdna.ssh.ssh_client import SSHClient
from kdna.server.server import directory_exists

@click.group()
def server():
    """Commande pour gérer les serveurs"""


#! Création des commandes du groupe server
# Création de la commande add
@server.command()
@click.option('-i', '--id', required=True, help="entrer l'id")
@click.option('-ad', '--address', required=True, help="entrer le libelé de connexion")
@click.option('-a', '--alias', required=True, help="entrer l'alias")
@click.option('-r', '--repo', required=True, help="entrer le répertoire de sauvegarde")
@click.option('-p', '--port', required=True, help="entrer le port")
def add(id, alias, address, repo, port):
    """Commande pour ajoute un serveur."""
    try:
        connection = SSHClient(address)
        connection.sendCommand("ls > /dev/null")

        try:
            connection.sendCommand(f"test ! -d {repo} && mkdir {repo}")
        except Exception:
            click.echo("Le dossier existe déjà")
        ServerService().create_server(id, address, repo, port, alias)
    except Exception as e:
        print(e)
        print("An errror occured connection on this adress fail.")
        return None



# Création de la commande delete
@server.command()
@click.option('-a', '--alias', required=False, help="entrer l'alias du serveur à supprimer")
@click.option('-i', '--id', required=False, help="entrer l'id du serveur à supprimer")
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
@click.argument('alias', required=True)
@click.option('-c', 'credentials', default='', required=False, help="entrer les nouvelles credentials")
@click.option('-p', 'port', default='', required=False, help="entrer le nouveau port")
@click.option('-ad', 'new_address', default='', required=False, help="entrer la nouvelle adresse")
@click.option('-a', 'new_alias', default='', required=False, help="entrer le nouvel alias")
def update(alias, credentials, port, new_address, new_alias):
    """
    Commande pour mettre à jour un serveur.\n
    argument obligatoire :\n
    \t- <alias>: l'alias du serveur à mettre à jour
    """
    serverService = ServerService()
    if alias and new_address or alias and credentials or alias and port or alias and new_alias:
        serverService.update_server(
            alias, credentials, port, new_address, new_alias)
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
        ['id', 'host', 'path', 'port', 'alias'],
        tablefmt="grid"
    )
    click.echo(table)


@server.command()
def status():
    click.echo("Server Status")
    
@server.command()
def import_s():
    """Import server from ~/.ssh/config file"""
    serverService = ServerService()
    serverService.import_server()
