"""
Groupe de commandes tag qui permet de gérer les tags
add: Commande pour créer un tag
list: Commande pour lister les tags
"""

import click

from kdna.logger.logger import log
from kdna.parsing import parser
from kdna.ssh.ssh_client import SSHClient
from kdna.tags import tags


@click.group()
def tag():
    """Commande pour gérer les tags"""


# ! Création des commandes du groupe tag
# Création de la commande add
@tag.command()
@click.option('-p', '--project', required=True, help="entrez le projet dans lequel ajouter le tag")
@click.option('-t', '--new_tag', required=True, help="entrez le tag à ajouter")
@click.option('-f', '--file_to_tag', required=True, help="entrez le fichier à tagger")
@click.option('-s', '--server', required=True, help="entrez l'id ou l'alias du serveur")
def add(project, new_tag, file_to_tag, server):
    """Commande pour ajouter un tag."""

    # serversCredential = listServers[0].credentials
    #   instance = SSHClient(serversCredential).connect()
    connection_instance = None
    list_servers = parser.listServers
    for server_i in list_servers:
        if server in (server_i.id_server, server_i.alias):
            connection_instance = SSHClient(server_i.credentials, server_i.path)
            connection_instance.connect()
            break

    if connection_instance is None:
        click.echo("Le serveur n'a pas été trouvé")
        log("ERROR", "Le serveur n'a pas été trouvé")
        raise click.Abort()

    try:
        tags.add_tags(connection_instance.connection, project, new_tag, file_to_tag)
    except FileNotFoundError:
        click.echo("Le fichier n'a pas été trouvé")
        log("ERROR", "Le fichier à ajouter n'a pas été trouvé")
    except PermissionError:
        click.echo("Vous n'avez pas les droits pour réaliser cette action")
        log("ERROR", "Vous n'avez pas les droits pour réaliser cette action")
    except Exception as e:
        print("Une erreur est survenue : " + e)
        log("ERROR", "An error occurred" + e)


# Création de la commande delete
@tag.command()
@click.option('-p', '--project', required=True, help="entrez le projet dans lequel ajouter le tag")
@click.option('-t', '--old_tag', required=True, help="entrez le tag à supprimer")
@click.option('-s', '--server', required=True, help="entrez l'id ou l'alias du serveur")
def delete(project, old_tag, server):
    """Commande pour supprimer un tag."""

    # serversCredential = listServers[0].credentials
    #   instance = SSHClient(serversCredential).connect()
    connection_instance = None
    list_servers = parser.listServers
    for server_i in list_servers:
        if server in (server_i.id_server, server_i.alias):
            connection_instance = SSHClient(server_i.credentials, server_i.path)
            connection_instance.connect()
            break

    if connection_instance is None:
        click.echo("Le serveur n'a pas été trouvé")
        log("ERROR", "Le serveur n'a pas été trouvé")
        raise click.Abort()

    try:
        tags.delete_tags(connection_instance.connection, project, old_tag)
        click.echo(f"Le tag {old_tag} a été supprimé")
    except FileNotFoundError:
        click.echo("Le fichier n'a pas été trouvé")
        log("ERROR", "Le fichier à supprimer n'a pas été trouvé")
    except PermissionError:
        click.echo("Vous n'avez pas les droits pour réaliser cette action")
        log("ERROR", "Vous n'avez pas les droits pour réaliser cette action")
    except Exception as e:
        print("Une erreur est survenue " + e)
        log("ERROR", "An error occurred " + e)


# Création de la commande update
@tag.command()
@click.option('-p', '--project', required=True, help="entrez le projet dans lequel ajouter le tag")
@click.option('-t', '--old_tag', required=True, help="entrez le tag à modifier")
@click.option('-n', '--new_tag', required=True, help="entrez le nouveau tag")
@click.option('-s', '--server', required=True, help="entrez l'id ou l'alias du serveur")
def update(project, old_tag, new_tag, server):
    """Commande pour modifier un tag."""

    connection_instance = None
    list_servers = parser.listServers
    for server_i in list_servers:
        if server in (server_i.id_server, server_i.alias):
            connection_instance = SSHClient(server_i.credentials, server_i.path)
            connection_instance.connect()
            break
    if connection_instance is None:
        click.echo("Le serveur n'a pas été trouvé")
        raise click.Abort()

    try:
        tags.update_tags(connection_instance.connection, project, old_tag, new_tag)
        click.echo(f"Le tag {old_tag} a été modifié en {new_tag}")
        log("INFO", "Tag " + old_tag + " has been modified to " + new_tag)
    except FileNotFoundError:
        click.echo("Le fichier n'a pas été trouvé")
        log("ERROR", "File to update not found")
    except PermissionError:
        click.echo("Vous n'avez pas les droits")
        log("ERROR", "You don't have the rights")
    except Exception as e:
        print("error = " + e)
        log("ERROR", "error = " + e)


# Création de la commande list
@tag.command()
@click.option('-p', '--project', required=True, help="entrez le projet du tag à supprimer")
@click.option('-s', '--server', required=True, help="entrez l'id ou l'alias du serveur")
def list(project, server):
    """Commande pour lister les tags."""

    connection_instance = None
    list_servers = parser.listServers
    for server_i in list_servers:
        if server in (server_i.id_server, server_i.alias):
            connection_instance = SSHClient(server_i.credentials, server_i.path)
            connection_instance.connect()
            break

    if connection_instance is None:
        click.echo("Le serveur n'a pas été trouvé")
        log("ERROR", "Le serveur n'a pas été trouvé")
        raise click.Abort()

    try:
        for (tag, backup) in tags.get_tag_conf(connection_instance.connection, project):
            click.echo(f"{tag} : {backup}")
    except FileNotFoundError:
        click.echo("Le fichier n'a pas été trouvé")
        log("ERROR", "Le fichier à supprimer n'a pas été trouvé")
    except PermissionError:
        click.echo("Vous n'avez pas les droits")
        log("ERROR", "Vous n'avez pas les droits pour réaliser cette action")
    except Exception as e:
        print("Une erreur est survenue" + e)
        log("ERROR", "An error occurred " + e)
