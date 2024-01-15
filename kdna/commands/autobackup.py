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


import subprocess
import click
from kdna.logger.logger import log  # Logging ability import
from kdna.server.autobackup_service import AutoBackupService  # kdna.conf C(R)UD import
from kdna.parsing.parser import parseConfig  # parser import
from kdna.tags import tags
from tabulate import tabulate  # tabulate import for list command. (prettier list)


# Fonctions CRUD pour le crond
# The crond (cron daemon) reads the cron tables to configure the schedule


def list_crontab():
    try:
        result = subprocess.run('crontab -l 2>&1 |grep -Ev "^(#|n)"', shell=True, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').split('\n')[:-1]
    except subprocess.CalledProcessError as e:
        click.echo(f"Error listing crontab: {e}")
        log(f"Error listing crontab: {e}")

def add_cron_job(command, schedule):
    try:
        subprocess.run(f'(crontab -l 2>&1 |grep -Ev "^(#|n)" ; echo "{schedule} {command}") |sort |uniq |crontab -', shell=True)
        click.echo("Cron job added successfully.")
        log("Cron job added successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error adding cron job: {e}")
        log(f"Error adding cron job: {e}")

def update_cron_job(command, new_schedule):
    try:
        delete_cron_job(command)
        add_cron_job(command, new_schedule)
        click.echo("Cron job updated successfully.")
        log("Cron job updated successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error updating cron job: {e}")
        log(f"Error updating cron job: {e}")

def delete_cron_job(command):
    try:
        subprocess.run(f'(crontab -l 2>&1 | grep -Ev " {command}$") |sort |uniq |crontab -', shell=True) 
        click.echo("Cron job deleted successfully.")
        log("Cron job deleted successfully.")
    except subprocess.CalledProcessError as e:
        click.echo(f"Error deleting cron job: {e}")
        log(f"Error deleting cron job: {e}")


def get_custom_cron(sched_part_type: str, cond_inf: int, cond_sup: int):
    """Fonction qui récupère auprès de l'utilisateur une partie de la date du schedule de custom_cron pour autobackup (e.g. renvoie la minute de backup, ou l'heure, ...).\n
    :param sched_part_type: le type de la partie manquante de custom_cron à demander à l'utilisateur (e.g. 'Hour')\n
    :sched_part_type sched_part_type: str\n
    :return: le custom_cron partiel\n
    :rsched_part_type: str
    """
    incorrect = True
    while incorrect:
        schedule_part = input(
            f">Entrez une valeur numérique comprise entre {cond_inf} et {cond_sup} (inclus) pour '{sched_part_type}', ou entrez 'help' pour afficher les correspondances : ")
        if schedule_part.lower() == "help":
            click.echo("Minute (0 - 59)\nHeure (0 - 23)\nJour du mois (1 - 31)\nMois (1 - 12)\nJour de la semaine (0 - 6) (dimanche est 0)\nNe rien entrer pour ne pas préciser.")
        elif schedule_part == '' or cond_inf <= int(schedule_part) <= cond_sup:
            incorrect = False
        else:
            click.echo("Entrée invalide, réessayez S.V.P")

    return schedule_part + ':'


def concatenate_custom_cron():
    custom_cron = get_custom_cron("Minute", 0, 59)
    custom_cron += get_custom_cron("Heure", 0, 23)
    custom_cron += get_custom_cron("Jour du mois", 1, 31)
    custom_cron += get_custom_cron("Mois", 1, 12)
    custom_cron += get_custom_cron("Jour de la semaine", 0, 6)
    return custom_cron[:-1]  # Suppression du ':' final


def validate_cron_schedule(custom_cron:str):
    schedule_list = custom_cron.split(':')
    if len(schedule_list) != 5:
        return False
    else:
        for part in schedule_list:  # Check that every part is made only of numbers
            if not (part.isnumeric() or part == ''):
                return False
        # Check that numbers are in the correct range
        if not (0 < int(schedule_list[0]) <= 59 and 0 < int(schedule_list[1]) <= 23 and 1 < int(schedule_list[2]) <= 31 and 1 < int(schedule_list[3]) <= 12 and 0 < int(schedule_list[4]) <= 6):
            return False
    return True


def translate_cron_schedule(cron_schedule):
    if cron_schedule == 'daily':
        return '0:0:::'
    elif cron_schedule == 'monthly':
        return '0:0:0::'
    elif cron_schedule == 'weekly':  # Every saturday at 00:00
        return '0:0:::6'
    else:
        return False


def reformat(custom_cron):
    # Translate '0:1:2::3' to '0 1 2 * 3'
    parts = custom_cron.split(':')

    # Use list comprehension to replace empty parts with '*'
    translated_parts = ['*' if not part else part for part in parts]

    # Join the translated parts with ' '
    result_string = ' '.join(translated_parts)

    return result_string


# Création des commandes du groupe autobackup

# Creation du groupe de commande autobackup
@click.group(name='auto-backup')
def autobackup():
    """Commande pour mettre en place un daemon de sauvegarde"""


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
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
            custom_cron = concatenate_custom_cron()  # le custom_cron est donc demandé en input interactif
            log("INFO", "Chosen custom cron schedule is :", custom_cron)
            click.echo("Chosen custom cron schedule is :", custom_cron)
        else:  # Cron schedule is not custom
            click.echo("L'argument custom_cron n'est pas au format '0-59:0-23:1-31:1-12:0-6'. Ne définissez pas l'option pour la définir interactivement.")
            log("ERROR", "Chosen custom cron schedule is :", custom_cron)
            click.echo("Chosen custom cron schedule is :", custom_cron)
    else:
        custom_cron = translate_cron_schedule(cron_schedule)
        log("INFO", "Chosen custom cron schedule is :", custom_cron)
        click.echo("Chosen custom cron schedule is :", custom_cron)
        if custom_cron == False:  # translate_cron_schedule() error
            click.echo("L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
            log("ERROR", "L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
    log("INFO", "Calling kdna.conf CRUD...")
    AutoBackupService().create_auto_backup(idcron, custom_cron, nameofcron, date, server, path)  # Écrit dans kdna.conf
    log("INFO", "Calling parser...")
    parseConfig()  # Lance le parseur
    log("INFO", "Writing crontab...")
    command = "kdna backup add " + project + ' ' + path + ' ' + tag
    schedule = reformat(custom_cron)
    add_cron_job(command, schedule)
    log("INFO", "Created cron schedule")
    print("Created cron schedule")


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
    delete_cron_job(command)
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
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
            custom_cron = concatenate_custom_cron()  # le custom_cron est donc demandé en input interactif
            log("INFO", "Chosen custom cron schedule is :", custom_cron)
            click.echo("Chosen custom cron schedule is :", custom_cron)
        else:  # Cron schedule is not custom
            click.echo("L'argument custom_cron n'est pas au format '0-59:0-23:1-31:1-12:0-6'. Ne définissez pas l'option pour la définir interactivement.")
            log("ERROR", "Chosen custom cron schedule is :", custom_cron)
            click.echo("Chosen custom cron schedule is :", custom_cron)
    else:
        custom_cron = translate_cron_schedule(new_cron_schedule)
        log("INFO", "Chosen custom cron schedule is :", custom_cron)
        click.echo("Chosen custom cron schedule is :", custom_cron)
        custom_cron = translate_cron_schedule(new_cron_schedule)
        if custom_cron == False:  # translate_cron_schedule() error
            click.echo("L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
    log("INFO", "Calling kdna.conf CRUD...")
    AutoBackupService().update_auto_backup(idcron, new_cron_schedule="", new_name="", new_date="", new_path="")  # Modifie kdna.conf
    log("INFO", "Calling parser...")
    parseConfig()  # Lance le parseur
    log("INFO", "Writing crontab...")
    command = "kdna backup add " + project + ' ' + new_path + ' ' + tag
    new_schedule = reformat(custom_cron)
    update_cron_job(command, new_schedule)
    log("INFO", "Updated cron schedule")
    print("Updated cron schedule")


# Création de la commande list
@autobackup.command()
def list():
    """Commande pour lister les autobackups\n
    :return: Liste des autobackups : class: `str`\n
    :rtype: list
    """
    autobackups = AutoBackupService().find_all()
    table = tabulate(
        [[data for data in autobackup.values()] for autobackup in autobackups],
        ['id', 'frequency', 'name', 'timestamp', 'id_server', 'path'],
        tablefmt="grid"
    )
    click.echo(table)
    click.echo(tabulate(list_crontab()))
    log("INFO", "Listed all autobackups")


# # Création de la commande stop
# @autobackup.command()
# @click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nom du cron à stopper")
# def stop(nameofcron):
#     """
#     Commande pour stopper une backup régulière\n
#     """
#     click.echo(f"Stopped cron : \"{nameofcron}\"")
