import click
from kdna.commands.backup import backup
from kdna.commands.server import server
from kdna.commands.autobackup import autobackup
from kdna.commands.encrypt import encrypt
from kdna.parsing.parser import parseConfig


@click.group()
def kdna():
    """"""


def main():
    parseConfig()
    kdna.add_command(backup)
    kdna.add_command(server)
    kdna.add_command(autobackup)
    kdna.add_command(encrypt)

    """main: Fonction principale"""
    kdna()


if __name__ == "__main__":
    main()
