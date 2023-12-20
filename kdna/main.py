import click
from kdna.commands.backup import backup
from kdna.commands.server import server
from kdna.commands.autobackup import autobackup
from kdna.encrypt import encrypt
from kdna.container.container import Container
from dependency_injector.wiring import inject, Provide
from kdna.commands.kdna import kdna

@click.group()
def kdna():
    """"""



def main():
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])

    kdna.add_command(backup)
    kdna.add_command(server)
    kdna.add_command(autobackup)

    """main: Fonction principale"""
    ##encrypt.load_key()
    #encrypt.cypher()
    #encrypt.decypher()
    #encrypt.cypher_folders("./out", "./encoded")
    #encrypt.decypher_folders("./encoded", "./decoded")
    kdna()




if __name__ == "__main__":
    main()
