import click
from kdna.conf_utils.server import Server
from kdna.container.container import Container
from dependency_injector.wiring import inject, Provide
from kdna.commands.kdna import kdna



@click.group()
def server():
    """server: Commande pour lancer le serveur"""


@server.command()
@click.option('--alias', is_flag=True, default=False)
@click.argument('name')
@inject
def set(name, alias, ssh_client: Container.ssh_client = Provide[Container.ssh_client]):
    """set: Commande pour sélectionner un serveur
        --name: option pour entrer le nom du serveur"""
    #click.echo(f"SSH Client - Host: {ssh_client.host}")
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