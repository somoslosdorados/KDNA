import click
from kdna.commands.backup import backup
from kdna.commands.server import server
from kdna.commands.autobackup import autobackup
from kdna.commands.encrypt import encrypt
from kdna.commands.tag import tag

@click.group()
def kdna():
    """"""

kdna.add_command(backup)
kdna.add_command(server)
kdna.add_command(autobackup)
kdna.add_command(encrypt)
kdna.add_command(tag)

