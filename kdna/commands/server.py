import click
from kdna.conf_utils.server import Server
@click.group()
def server():
    """server: Commande pour lancer le serveur"""

@server.command()
@click.argument('name')
def set(name):
    """set: Commande pour sélectionner un serveur
        --name: option pour entrer le nom du serveur"""
    click.echo(f"Name {name}")
    server = Server("18", "creds", "22", "draco")
    server.add()
    print(server)