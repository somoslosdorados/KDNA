import click
from kdna.conf_utils.server import Server
from kdna.server.server_service import ServerService

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
@click.argument('name')
def add(name):
    #Todo ServerService create
    click.echo("FAUT IMPLEMENTER LES GARS")

@server.command()
@click.argument('id')
@click.option('--alias', is_flag=True, default=False)
def delete(id, alias):
    serverService = ServerService()
    serverService.delete_server(id, alias)
    click.echo(f"Id {id} - supprimé par alias : {alias}")

@server.command()
def status():
    click.echo("Server Status")


@server.command()
@click.argument('id')
@click.option('--address', '-a')
@click.option('--credentials', '-c')
@click.option('--port', '-p')
@click.option('--alias', '-na')
def update(id, address, credentials, port, alias):
    click.echo(f"old alias {id}, {address}, {credentials}, {port}, {alias}")
    serverService = ServerService()
    serverService.update_server(id, credentials, port, address, alias)
