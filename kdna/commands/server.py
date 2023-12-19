import click
from kdna.conf_utils.server import Server
from kdna.server.server_service import ServerService

@click.group()
def server():
    """Commande pour lancer le serveur"""


#! Création des commandes du groupe server
# Création de la commande set
@server.command()
@click.option('-i', '--id', required=True, help="entrer l'id")
@click.option('-a', '--alias', required=True, help="entrer l'alias")
@click.option('-c', '--credentials', required=True, help="entrer les credentials")
@click.option('-p', '--port', required=True, help="entrer le port")
def set(id, alias, credentials, port):
    """Commande pour sélectionner un serveur.\n
    :param id: -i l'id du serveur à séléctionner\n
    :type id: str\n
    :param alias: -a l'alias du serveur à sélectionner\n
    :type alias: str\n
    :param credentials: -c les credentials du serveur à sélectionner\n
    :type credentials: str\n
    :param port: -p le port du serveur à sélectionner\n
    :type port: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    if alias:
        click.echo(f"Alias du serveur : \"{alias}\"")
    if id:
        click.echo(f"ID du serveur : \"{id}\"")


# Création de la commande delete
@server.command()
@click.option('-a', '--alias', required=False, help="entrer l'alias du serveur à supprimer")
@click.option('-i', '--id', required=False, help="entrer l'id du serveur à supprimer")
def delete(alias, id):
    """Commande pour supprimer un serveur.\n
    :param alias: -a l'alias du serveur à supprimer\n
    :type alias: str\n
    :param id: -i l'ID du serveur à supprimer\n
    :type id: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
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
    :param alias: l'alias du serveur à mettre à jour\n
    :type alias: str\n
    :param credentials: -c les nouvelles credentials\n
    :type credentials: str\n
    :param port: -p le nouveau port\n
    :type port: str\n
    :param new_alias: -a le nouvel alias\n
    :type new_alias: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    if alias:
        click.echo(f"Serveur mis à jour : \"{alias}\"")

# Création de la commande list
@server.command()
def list():
    """Commande pour lister les serveurs\n
    :return: Liste des serveurs : class: `str`\n
    :rtype: list"""
    click.echo(f"List of server : \n...\n...")