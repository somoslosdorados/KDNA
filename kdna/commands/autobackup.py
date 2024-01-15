"""
This is the autoback Click commands program. It implements the Click commands function to make auto-backups.

Authors: Théo TCHILINGUIRIAN

Groupe de commandes auto-backup qui permet de gérer les auto-backups (backups régulières)
schedule : Commande pour prévoir une auto-backup
delete : Commande pour supprimer une auto-backup
update : Commande pour mettre à jour une auto-backup
stop : Commande pour stopper une auto-backup
list : Commande pour lister les auto-backups
"""


import click
from kdna.logger.logger import log  # Logging ability import
# kdna.conf C(R)UD import
from kdna.server.autobackup_service import AutoBackupService
from kdna.parsing.parser import parseConfig  # parser import
import kdna.autobackup.autobackup
# tabulate import for list command. (prettier list)
from tabulate import tabulate


# Fonctions CRUD pour le crond
# The crond (cron daemon) reads the cron tables to configure the schedule


# Création des commandes du groupe autobackup

# Creation du groupe de commande autobackup
@click.group(name='auto-backup')
def autobackup():
    """Commande pour mettre en place un daemon de sauvegarde"""

# TODO : test custom cron schedule
# Création de la commande schedule


@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron")
@click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nom du cron")
@click.option('-p', '--project', nargs=1, required=True, help="entrer le nom du projet")
@click.option('-t', '--tag', nargs=1, required=True, help="entrer le tag")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly', 'custom']), required=True)
@click.argument('custom_cron', nargs=-1)
@click.option('-d', '--date', nargs=1, required=True, help="entrer la date de la première backup [ xxxx-xx-xx ]")
@click.option('-s', '--server', nargs=1, required=True, help="entrer l'id du serveur")
@click.option('-h', '--path', nargs=1, required=True, help="entrer le chemin de la backup")
def create(idcron, nameofcron, project, tag, cron_schedule, custom_cron, date, server, path):
    """
    Commande pour prévoir une auto-backup.\n
    Arguments obligatoires :\n
        \t- <cron_schedule>: le schedule de la backup (daily, monthly, weekly, custom)\n
        \t- <custom_cron>: le schedule personnalisé de l'auto-backup, obligatoire si l'option custom a été séléctionnée\n
        \tSi l'argument n'a pas été saisi, le programme rentre en mode interactif et attend des entrées de l'utilisateur pour compléter custom_cron.
    """
    log("INFO", "Creating a new auto-backup")
    log("INFO", f"Name of cron : \"{nameofcron}\"")
    log("INFO", f"Cron schedule choice : \"{cron_schedule}\"")
    click.echo(f"Name of cron : \"{nameofcron}\"")
    click.echo(f"Cron schedule choice : \"{cron_schedule}\"")

    if cron_schedule == 'custom':
        if not custom_cron:  # custom_cron n'est pas donné en argument
            click.echo(
                "L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
            # le custom_cron est donc demandé en input interactif
            custom_cron = kdna.autobackup.autobackup.concatenate_custom_cron()
            log("INFO", f"Chosen custom cron schedule is : {custom_cron}")
            click.echo(
                "INFO", f"Chosen custom cron schedule is : {custom_cron}")
        else:  # Cron schedule is not custom
            click.echo(
                "L'argument custom_cron n'est pas au format '0-59:0-23:1-31:1-12:0-6'. Ne définissez pas l'option pour la définir interactivement.")
            log("ERROR", f"Chosen custom cron schedule is : {custom_cron}")
            click.echo(f"Chosen custom cron schedule is : {custom_cron}")
    else:
        custom_cron = kdna.autobackup.autobackup.translate_cron_schedule(
            cron_schedule)
        log("INFO", f"Chosen custom cron schedule is : {custom_cron}")
        click.echo(f"Chosen custom cron schedule is : {custom_cron}")
        if custom_cron == False:  # translate_cron_schedule() error
            click.echo(
                "L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
            log("ERROR",
                "L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
    log("INFO", "Calling kdna.conf CRUD...")

    schedule = kdna.autobackup.autobackup.reformat(custom_cron)

    try:
        AutoBackupService().create_auto_backup(idcron, schedule, nameofcron,
                                               date, server, path)  # Écrit dans kdna.conf
    except Exception as e:
        click.echo(e)
        return

    log("INFO", "Calling parser...")
    parseConfig()  # Lance le parseur
    log("INFO", "Writing crontab...")
    command = "kdna backup add " + project + ' ' + path + ' ' + tag
    kdna.autobackup.autobackup.add_cron_job(command, schedule)
    log("INFO", "Created cron schedule")


# Création de la commande delete
@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron (de l'autobackup) à supprimer")
@click.option('-p', '--project', nargs=1, required=True, help="entrer le nom du projet")
@click.option('-t', '--tag', nargs=1, required=True, help="entrer le tag")
@click.option('-h', '--path', nargs=1, required=True, help="entrer le chemin de la backup")
def delete(idcron, project, tag, path):
    """
    Commande pour supprimer une backup régulière
    """
    log("INFO", "Calling kdna.conf CRUD...")
    AutoBackupService().delete_auto_backup(idcron)
    log("INFO", f"Deleted cron : \"{idcron}\"")
    click.echo(f"Deleted cron : \"{idcron}\"")
    log("INFO", "Calling parser...")
    parseConfig()  # Lance le parseur
    log("INFO", "Writing crontab...")
    command = "kdna backup add " + project + ' ' + path + ' ' + tag
    kdna.autobackup.autobackup.delete_cron_job(command)
    log("INFO", "Deleted cron schedule")
    print("Deleted cron schedule")


@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron à mettre à jour")
@click.option('-p', '--project', nargs=1, required=True, help="entrer le nom du projet à mettre à jour")
@click.option('-t', '--tag', nargs=1, required=True, help="entrer le tag à mettre à jour")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly', 'custom']), required=False)
@click.argument('custom_cron', nargs=-1, required=False)
@click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nouveau nom du cron")
@click.option('-d', '--date', nargs=1, required=False, help="entrer la nouvelle date de la première backup [ xxxx-xx-xx ]")
@click.option('-h', '--path', nargs=1, required=False, help="entrer le chemin de la nouvelle backup")
def update(idcron, project, tag, new_cron_schedule="", custom_cron="", new_name="", new_date="", new_path=""):
    """
            Commande pour mettre à jour une backup régulière\n
            \t- <cron_schedule> : le schedule de l'auto-backup à mettre à jour ['daily', 'monthly', 'weekly', 'custom']\n
            \t- <custom_cron> : le schedule personnalisé à mettre à jour de l'auto-backup, obligatoire si l'option custom a été séléctionnée\n
            \tSi l'argument n'a pas été saisi, le programme rentre en mode interactif et attend des entrées de l'utilisateur pour compléter custom_cron.
    """
    log("INFO", f"Name of cron : \"{idcron}\"")
    log("INFO", f"New cron schedule : \"{new_cron_schedule}\"")
    click.echo(f"Name of cron : \"{idcron}\"")
    click.echo(f"New cron schedule : \"{new_cron_schedule}\"")
    if new_cron_schedule == 'custom':
        if not custom_cron:  # custom_cron n'est pas donné en argument
            click.echo(
                "L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
            # le custom_cron est donc demandé en input interactif
            custom_cron = kdna.autobackup.autobackup.concatenate_custom_cron()
            log("INFO", "Chosen custom cron schedule is :", custom_cron)
            click.echo("Chosen custom cron schedule is :", custom_cron)
        else:  # Cron schedule is not custom
            click.echo(
                "L'argument custom_cron n'est pas au format '0-59:0-23:1-31:1-12:0-6'. Ne définissez pas l'option pour la définir interactivement.")
            log("ERROR", "Chosen custom cron schedule is :", custom_cron)
            click.echo("Chosen custom cron schedule is :", custom_cron)
    else:
        custom_cron = kdna.autobackup.autobackup.translate_cron_schedule(
            new_cron_schedule)
        log("INFO", "Chosen custom cron schedule is :", custom_cron)
        click.echo("Chosen custom cron schedule is :", custom_cron)
        custom_cron = kdna.autobackup.autobackup.translate_cron_schedule(
            new_cron_schedule)
        if not custom_cron:  # translate_cron_schedule() error
            click.echo(
                "L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
    log("INFO", "Calling kdna.conf CRUD...")
    AutoBackupService().update_auto_backup(idcron, new_cron_schedule="",
                                           new_name="", new_date="", new_path="")  # Modifie kdna.conf
    log("INFO", "Calling parser...")
    parseConfig()  # Lance le parseur
    log("INFO", "Writing crontab...")
    command = "kdna backup add " + project + ' ' + new_path + ' ' + tag
    new_schedule = kdna.autobackup.autobackup.reformat(custom_cron)
    kdna.autobackup.autobackup.update_cron_job(command, new_schedule)
    log("INFO", "Updated cron schedule")


# Création de la commande list
@autobackup.command()
def list():
    """Commande pour lister les autobackups\n
    :return: Liste des autobackups : class: `str`\n
    :rtype: list
    """
    autobackups = AutoBackupService().find_all()
    print(autobackups)
    table = tabulate(
        [[data for data in autobackup.values()] for autobackup in autobackups],
        ['id', 'frequency', 'name', 'timestamp', 'id_server', 'path'],
        tablefmt="grid"
    )
    click.echo(table)
    log("INFO", "Listed all autobackups")
