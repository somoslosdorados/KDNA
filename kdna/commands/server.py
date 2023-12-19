import click
from kdna.conf_utils.server import Server
@click.group()
def server():
    """Commande pour lancer le serveur"""

#! Création des commandes du groupe server
# Création de la commande set
@server.command()
@click.argument('alias', default='')
@click.argument('id', default='')
def set(alias, id):
    """Commande pour sélectionner un serveur.\n
    param alias: l'alias du serveur à sélectionner\n
    :type alias: str\n
    :param id: l'id du serveur à séléctionner\n
    :type id: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    if alias:
        click.echo(f"Alias du serveur : \"{alias}\"")
    if id:
        click.echo(f"ID du serveur : \"{id}\"")

# Création de la commande add
@server.command()
@click.argument('alias', nargs=1, required=True)
@click.argument('port', nargs=1, required=True, type=str)
@click.argument('userip', nargs=1, required=True, type=str)
def add(alias, port, userip):
    """Commande pour ajouter un serveur\n:
    param alias: l'alias du serveur à ajouter\n
    :type alias: str\n
    :param port: le port du serveur à supprimer\n
    :type port: str\n
    :param userip: l'utilisateur et l'ip du serveur à supprimer --> user@ip\n
    :type userip: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    click.echo(f"Added server with alias : \"{alias}\", port : \"{port}\", and user@ip : \"{userip}\"")

# Création de la commande delete
@server.command()
@click.argument('alias', default='')
@click.argument('id', default='')
def delete(alias, id):
    """Commande pour supprimer un serveur.\n
    :param alias: l'alias du serveur à supprimer\n
    :type alias: str\n
    :param id: l'ID du serveur à supprimer\n
    :type id: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    if alias:
        click.echo(f"Suppression du serveur : \"{alias}\"")
    if id:
        click.echo(f"Suppression du serveur : \"{id}\"")

# Création de la commande list
@server.command()
def list():
    """Commande pour lister les serveurs\n
    :return: Liste des serveurs : class: `str`\n
    :rtype: list"""
    click.echo(f"List of server : \n...\n...")