import click

@click.group()
def backup():
    """backup: Commande pour sauvegarder un fichier"""

@backup.command()
@click.option('-t', '--namepath', nargs=2, help="entrer le nom et le chemin du fichier à sauvegarder")
def add(namepath):
    name, path = namepath
    click.echo(f"Created backup \"{name}\":v1.1.2")

