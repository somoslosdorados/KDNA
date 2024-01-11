"""
Groupe de commandes tag qui permet de gérer les tags
add: Commande pour créer un tag
list: Commande pour lister les tags
"""

import click
from kdna.server.server_service import ServerService
from kdna.parsing.parser import listServers
from tabulate import tabulate
from kdna.ssh.ssh_client import SSHClient
from kdna.tags import tags
ssh = SSHClient("test@debian12.local",[])
ssh.connect()


@click.group()
def tag():
    """Commande pour gérer les tags"""


#! Création des commandes du groupe tag
# Création de la commande add
@tag.command()
@click.option('-p', '--project', required=True, help="entrer le projet dans lequel ajouter le tag")
@click.option('-t', '--new_tag', required=True, help="entrer le tag à ajouter")
@click.option('-f', '--file_to_tag', required=True, help="entrer le fichier à tagger")
def add(project, new_tag, file_to_tag):
    """Commande pour ajouter un tag."""

#serversCredential = listServers[0].credentials
 #   instance = SSHClient(serversCredential).connect()

    try:
        tags.add_tags(ssh.connection, project, new_tag, file_to_tag, True)
    except FileNotFoundError as exc:
        click.echo("Le fichier n'a pas été trouvé")
    except PermissionError as exc:
        click.echo("Vous n'avez pas les droits")
    except Exception as e:
        print("error = "+e.__str__())


# Création de la commande list
@tag.command()
@click.option('-p', '--project', required=True, help="entrer le projet du tag à supprimer")
def list(project):
    """Commande pour lister les tags."""

    try:
        for (tag,backup) in tags.get_tag_conf(ssh.connection, project):
            click.echo(f"{tag} : {backup}")
    except FileNotFoundError as exc:
        click.echo("Le fichier n'a pas été trouvé")
    except PermissionError as exc:
        click.echo("Vous n'avez pas les droits")
    except Exception as e:
        print("error = "+e.__str__())
