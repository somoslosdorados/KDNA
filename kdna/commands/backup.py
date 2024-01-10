import click
import uuid
import os
import kdna.tags.tags as tags
from kdna.parsing.parser import listServers
from kdna.encrypt import encrypt
from kdna.parsing.parser import kdna_path
from kdna.ssh.ssh_client import SSHClient
from kdna.server.server import upload_file, download_file, find_path
from kdna.read_backups.agent import list_backups

# Creation du groupe de commande backup


@click.group()
def backup():
    """Commande pour sauvegarder un fichier"""


# Création de la fonction display pour afficher le contenu d'un fichier
def display(path):
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Fichier non trouvé") from exc

    except PermissionError as exc:
        raise PermissionError("Oups, Pas les droits") from exc


# Création des commandes du groupe backup

# Création de la commande add
@backup.command()
@click.argument('project', nargs=1, required=True)
@click.argument('path', nargs=1, required=True)
@click.argument('tag', nargs=1, required=True)
def add(project, path, tag):
    click.echo(f"Creating backup \"{project}\":\n{tag}")
    uuid_backup = str(uuid.uuid4())
    name_of_temp_backup = encrypt.package(path, uuid_backup, kdna_path, True)
    path_to_local_backup = os.path.join(kdna_path, name_of_temp_backup)
    path_to_remote_backup = os.path.join("kdna", "project")
    serversCredential = listServers[0].credentials
    try:
        instance = SSHClient(serversCredential).connect()
    except Exception as e:
        print("error2 = "+e.__str__())

    try:
        upload_file(instance.connection, path_to_local_backup,
                    path_to_remote_backup)
        os.remove(path_to_local_backup)
        tags.addTags(instance.connection, "project",
                     tag, name_of_temp_backup, True)
    except Exception as e:
        print("error = "+e.__str__())

# Création de la commande delete


@backup.command()
@click.option('-t', 'pathtag', nargs=1, required=True, help="entrer le path du fichier et le tag [ path:tag ]")
def delete(pathtag):
    click.echo(f"Suppression du fichier : \"{pathtag}\"")

@backup.command()
@click.option('-pt', 'pathtag', nargs=1, required=True, help="entrer le path du fichier et le tag [ path:tag ]")
@click.option('-t', '--tag', nargs=2, required=False, help="entrer le tag de la backup à mettre à jour et le tag mis à jour")
@click.option('-p', '--path', nargs=1, required=False, help="entrer le chemin de la nouvelle backup")
def update(idcron, tag, cron_schedule, custom_cron, date, path):
    old_tag, new_tag = tag
    click.echo(f"Name of cron : \"{idcron}\"")
    click.echo(f"Cron tag and schedule : \"{tag}\" \"{cron_schedule}\"")
    if cron_schedule == 'custom':
        if not custom_cron:
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
        else:
            click.echo(f"Custom cron : \"{custom_cron}\"")


# Création de la commande list
@backup.command()
@click.argument('project_name', nargs=1, required=True)
def list(project_name):
    try:
        instance = SSHClient(listServers[0].credentials).connect()
    except Exception as e:
        print("error = "+e.__str__())

    backups = []

    try:
        backups = list_backups(instance.connection, project_name)
        tags.readTags(instance.connection, project_name)
    except Exception as e:
        print("error2 = "+e.__str__())

    if backups is None:
        click.echo(f'Project {project_name} not found')
    # else:
        # click.echo('Backups : ' + str(backups))
        # click.echo('Tags : ' + str(backups))


# Création de la commande restore
@backup.command()
@click.option('-t', '--nametag', nargs=1, required=True,
              help="entrer le nom du fichier à restaurer et le tag [ name:tag ]")
@click.argument('path', nargs=1, required=True)
def restore(nametag, path):
    click.echo(f"Restauration du fichier : \"{nametag}\"")

    try:
        instance = SSHClient(listServers[0].credentials).connect()
    except Exception as e:
        print(e)

    remote_path = find_path(instance.connection, nametag, "project")

    local_temp_path = os.path.join(
        kdna_path, "temp", remote_path.split("/")[-1])

    try:
        download_file(
            instance.connection, local_temp_path, remote_path)
    except Exception as e:
        print(e)

    try:
        restored_path = encrypt.restore(local_temp_path, path)
    except Exception as e:
        print(e)

    click.echo(f"Restauration faite : \"{restored_path}\"")
    os.remove(local_temp_path)
