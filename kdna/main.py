import click
from commands.backup import backup
from commands.server import server
from commands.autobackup import autobackup
from encrypt.encrypt import encrypt_archive, decrypt_archive
from encrypt import encrypt

@click.group()
def kdna():
    """kdna : Commande principale"""
    kdna.add_command(backup)
    kdna.add_command(server)
    kdna.add_command(autobackup)

def main():
    """main: Fonction principale"""
    encrypt.load_key()
    encrypt.cyper()
    encrypt.decypher()
    encrypt.cypher_folders("./out", "./encoded")
    encrypt.decypher_folders("./encoded", "./decoded")
    kdna()


if __name__ == "__main__":
    main()
