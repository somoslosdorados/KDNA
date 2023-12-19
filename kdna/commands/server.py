import click
from kdna.conf_utils.server import Server
@click.group()
def server():
    """server: Commande pour lancer le serveur"""

@server.command()
@click.argument('name')
@click.option('--alias', is_flag=True, default=False)
def set(name, alias):
    """set: Commande pour sélectionner un serveur
        --name: option pour entrer le nom du serveur"""
    if alias:
        click.echo(f"Sélection du server {name} par l'alias")
    else:
        click.echo(f"Sélection du server {name} par l'id")


@server.command()
@click.argument('id')
@click.option('--alias', is_flag=True, default=False)
def delete(id, alias):
    click.echo(f"Id {id} - supprimé par alias : {alias}")
    Server.delete(id, alias)

# Création de la commande delete
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
@click.argument('id')
@click.option('--alias', is_flag=True, default=False)
def delete(id, alias):
    click.echo(f"Id {id} - supprimé par alias : {alias}")
    Server.delete(id, alias)

@server.command()
def status():
    click.echo("Server Status")