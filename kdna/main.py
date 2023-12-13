import click
from commands.backup import backup
from commands.server import server
from commands.autobackup import autobackup

@click.group()
def kdna():
    """kdna : Commande principale"""

kdna.add_command(backup)
kdna.add_command(server)
kdna.add_command(autobackup)

def main():
    """main: Fonction principale"""
    kdna()

if __name__ == '__main__':
    main()