import click
from kdna.commands.backup import backup
from kdna.commands.server import server
from kdna.commands.autobackup import autobackup
from kdna.commands.tag import tag
from kdna.encrypt import encrypt
from kdna.conf_utils.utils import Utils

@click.group()
def kdna():
    """"""

def main():
    Utils.initialize_config_file()
    kdna.add_command(backup)
    kdna.add_command(server)
    kdna.add_command(autobackup)
    kdna.add_command(tag)

    """main: Fonction principale"""
    kdna()
    
    
if __name__ == "__main__":
    main()
