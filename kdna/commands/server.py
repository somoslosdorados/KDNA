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