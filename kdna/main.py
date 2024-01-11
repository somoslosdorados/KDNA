import click
from kdna.commands.backup import backup
from kdna.commands.server import server
from kdna.commands.autobackup import autobackup
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

    """main: Fonction principale"""
    kdna()
    
    
if __name__ == "__main__":
    main()
