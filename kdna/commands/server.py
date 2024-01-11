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

@click.group()
def server():
    """Commande pour lancer le serveur"""


# Création des commandes du groupe server
# Création de la commande set
@server.command()
@click.option('-i', '--id', required=True, help="entrer l'id")
@click.option('-a', '--alias', required=True, help="entrer l'alias")
@click.option('-c', '--credentials', required=True, help="entrer les credentials")
@click.option('-p', '--port', required=True, help="entrer le port")
def set(id, alias, credentials, port):
    """Commande pour sélectionner un serveur."""
    if alias:
        click.echo(f"Alias du serveur : \"{alias}\"")
    if id:
        click.echo(f"ID du serveur : \"{id}\"")


# Création de la commande delete
@server.command()
@click.option('-a', '--alias', required=False, help="entrer l'alias du serveur à supprimer")
@click.option('-i', '--id', required=False, help="entrer l'id du serveur à supprimer")
def delete(alias, id):
    """Commande pour supprimer un serveur."""
    if alias:
        click.echo(f"Suppression du serveur : \"{alias}\"")
    else:
        if id:
            click.echo(f"Suppression du serveur : \"{id}\"")
        else:
            click.echo("L'argument alias ou id doit être renseigné.")

# Création de la commande update


@server.command()
@click.argument('alias', required=True)
@click.option('-c', 'credentials', default='', required=False, help="entrer les nouvelles credentials")
@click.option('-p', 'port', default='', required=False, help="entrer le nouveau port")
@click.option('-a', 'new_alias', default='', required=False, help="entrer le nouvel alias")
def update(alias, credentials, port, new_alias):
    """Commande pour mettre à jour un serveur.\n
    argument obligatoire :\n
    \t- <alias>: l'alias du serveur à mettre à jour"""
    if alias:
        click.echo(f"Serveur mis à jour : \"{alias}\"")

# Création de la commande list


@server.command()
def list():
    """Commande pour lister les serveurs"""
    serverService = ServerService()
    servers = serverService.find_all()

    table = tabulate(
        [[data for data in server.values()] for server in servers],
        ['id', 'host', 'credentials', 'port', 'alias'],
        tablefmt="grid"
    )
    click.echo(table)


@server.command()
def status():
    click.echo("Server Status")
