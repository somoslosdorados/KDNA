import click

@click.group()
def server():
    """server: Commande pour lancer le serveur"""

@server.command()
@click.argument('name')
def set(name):
    """set: Commande pour sélectionner un serveur
        --name: option pour entrer le nom du serveur"""
    click.echo(f"Name {name}")