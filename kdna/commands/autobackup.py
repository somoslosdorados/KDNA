"""
Groupe de commandes auto-backup qui permet de gérer les auto-backups (backups régulières)
schedule : Commande pour prévoir une auto-backup
delete : Commande pour supprimer une auto-backup
update : Commande pour mettre à jour une auto-backup
stop : Commande pour stopper une auto-backup
list : Commande pour lister les auto-backups
"""

import os
import subprocess
import click
from kdna.logger.logger import log
from kdna.server.autobackup_service import AutoBackupService  # import du C(R)UD de kdna.conf
from kdna.parsing.parser import parseConfig  # import du parseur
from kdna.tags import tags
from tabulate import tabulate


# Fonctions CRUD pour le crond
# The crond (cron daemon) reads the cron tables to configure the schedule

def create_cron_job(schedule, command):
    current_user = os.getlogin()
    cron = CronTab("")
    job = cron.new(command=command)
    job.setall(schedule)
    cron.write()

def read_cron_jobs():
    cron = CronTab(user='your_username')
    jobs = cron.find_comment('your_comment')  # Use a comment to identify your jobs
    return [(job.comment, job.command, str(job.slices)) for job in jobs]

def update_cron_job(old_command, new_command, new_schedule):
    cron = CronTab(user='your_username')
    jobs = cron.find_command(old_command)
    
    for job in jobs:
        job.set_command(new_command)
        job.setall(new_schedule)
    
    cron.write()

def delete_cron_job(command):
    cron = CronTab(user='your_username')
    jobs = cron.find_command(command)
    
    for job in jobs:
        cron.remove(job)
    
    cron.write()

# Create a new cron job
create_cron_job("0 2 * * *", "python /path/to/your/script.py")  # Run every day at 2:00 AM

# Read all cron jobs
jobs = read_cron_jobs()
for job in jobs:
    print(f"Command: {job[1]}, Schedule: {job[2]}")

# Update an existing cron job
update_cron_job("python /path/to/your/script.py", "python /path/to/your/updated_script.py", "30 1 * * *")  # Run every day at 1:30 AM

# Delete a cron job
delete_cron_job("python /path/to/your/updated_script.py")



# Fonctions CRUD pour le crond
# The crond (cron daemon) reads the cron tables to configure the schedule

def create_cron_job(schedule, command):
    current_user = os.getlogin()
    cron = CronTab("")
    job = cron.new(command=command)
    job.setall(schedule)
    cron.write()

def read_cron_jobs():
    cron = CronTab(user='your_username')
    jobs = cron.find_comment('your_comment')  # Use a comment to identify your jobs
    return [(job.comment, job.command, str(job.slices)) for job in jobs]

def update_cron_job(old_command, new_command, new_schedule):
    cron = CronTab(user='your_username')
    jobs = cron.find_command(old_command)
    
    for job in jobs:
        job.set_command(new_command)
        job.setall(new_schedule)
    
    cron.write()

def delete_cron_job(command):
    cron = CronTab(user='your_username')
    jobs = cron.find_command(command)
    
    for job in jobs:
        cron.remove(job)
    
    cron.write()

# Create a new cron job
create_cron_job("0 2 * * *", "python /path/to/your/script.py")  # Run every day at 2:00 AM

# Read all cron jobs
jobs = read_cron_jobs()
for job in jobs:
    print(f"Command: {job[1]}, Schedule: {job[2]}")

# Update an existing cron job
update_cron_job("python /path/to/your/script.py", "python /path/to/your/updated_script.py", "30 1 * * *")  # Run every day at 1:30 AM

# Delete a cron job
delete_cron_job("python /path/to/your/updated_script.py")


from kdna.server.autobackup_service import AutoBackupService

# Creation du groupe de commande autobackup
@click.group(name='auto-backup')
def autobackup():
    """Commande pour mettre en place un daemon de sauvegarde"""


def get_type_cron(cron):
    for char in cron:
        if char == ':':
            return ':'
        elif char == '-':
            return '-'
    return -1


def is_valid_cron(cron):
    print(get_type_cron(cron))  # test pour voir à quoi ressemble la variable cron
    if get_type_cron(cron) == ':':
        cron_parts = cron.split(':')
        if len(cron_parts) != 5:
            return False
        if 0 >= cron_parts[0] <= 59 and 0 >= cron_parts[1] <= 23 and 1 >= cron_parts[2] <= 31 and 1 >= cron_parts[
            3] <= 12:
            return True
        return False
    elif get_type_cron(cron) == '-':
        cron_parts = cron.split(':')
        if len(cron_parts) != 5:
            return False
        if 0 >= cron_parts[0] <= 59 and 0 >= cron_parts[1] <= 23 and 1 >= cron_parts[2] <= 31 and 1 >= cron_parts[
            3] <= 12:
            return True
        return False
    else:
        return False


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


# Création des commandes du groupe autobackup

# Création de la commande schedule
@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron")
@click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nom du cron")
#@click.option('-p', '--project', nargs=1, required=True, help="entrer le nom du projet")
#@click.option('-t', '--tag', nargs=1, required=True, help="entrer le tag")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly', 'custom']), required=True)
@click.argument('custom_cron', nargs=-1)
@click.option('-d', '--date', nargs=1, required=True, help="entrer la date de la première backup [ xxxx-xx-xx ]")
@click.option('-s', '--server', nargs=1, required=True, help="entrer l'id du serveur")
@click.option('-p', '--path', nargs=1, required=True, help="entrer le chemin de la backup")
def create(idcron, nameofcron, project, tag, cron_schedule, custom_cron, date, server, path):
    """
    Commande pour prévoir une auto-backup.\n
    Arguments obligatoires :\n
        \t- <cron_schedule>: le schedule de la backup (daily, monthly, weekly, custom)\n
        \t- <custom_cron>: le schedule personnalisé de l'auto-backup, obligatoire si l'option custom a été séléctionnée\n
        \tSi l'argument n'a pas été saisi, le programme rentre en mode interactif et attend des entrées de l'utilisateur pour compléter custom_cron.
    """
    log("Info", "Creating a new auto-backup")
    log("Info", f"Name of cron : \"{nameofcron}\"")
    log("Info", f"Cron schedule choice : \"{cron_schedule}\"")
    if cron_schedule == 'custom':
        if not custom_cron:  # custom_cron n'est pas donné en argument
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
            custom_cron = concatenate_custom_cron()  # le custom_cron est donc demandé en input interactif
            log("Info", "Chosen custom cron schedule is :", custom_cron)
        else:  # Cron schedule is not custom
            click.echo("L'argument custom_cron n'est pas au format '0-59:0-23:1-31:1-12:0-6'. Ne définissez pas l'option pour la définir interactivement.")
            log("Error", "Chosen custom cron schedule is :", custom_cron)
    else:
        custom_cron = translate_cron_schedule(cron_schedule)
        log("Info", "Cron schedule is : \"{cron_schedule}\"")
        if custom_cron == False:  # translate_cron_schedule() error
            click.echo("L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
    log("Info", "Calling kdna.conf CRUD...")
    AutoBackupService().create_auto_backup(idcron, custom_cron, nameofcron, date, server, path)  # Écrit dans kdna.conf
    log("Info", "Calling parser...")
    parseConfig()  # Lance le parseur
    log("Info", "Writing crontab...")
    #create_cron_job 
    #tags.add_tags(project, tag, os.path.basename(path))


# Création de la commande delete
@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron (de l'autobackup) à supprimer")
def delete(idcron):
    """
    Commande pour supprimer une backup régulière
    """
    log("Info", "Calling kdna.conf CRUD...")
    AutoBackupService().delete_auto_backup(idcron)
    log("Info", f"Deleted cron : \"{idcron}\"")
    log("Info", "Calling parser...")
    parseConfig()  # Lance le parseur


@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron à mettre à jour")
#@click.option('-t', '--tag', nargs=2, required=False, help="entrer le tag du cron à mettre à jour et le tag mis à jour")
@click.option('-t', '--tag', nargs=1, required=False, help="entrer le tag du cron à mettre à jour")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly',
                                                    'custom']), required=False)
@click.argument('custom_cron', nargs=-1, required=False)
@click.option('-d', '--date', nargs=1, required=False,
              help="entrer la nouvelle date de la première backup [ xxxx-xx-xx ]")
@click.option('-p', '--path', nargs=1, required=False, help="entrer le chemin de la nouvelle backup")
def update(idcron, new_cron_schedule="", custom_cron="", new_date="", new_path=""):
    """
            Commande pour mettre à jour une backup régulière\n
            \t- <cron_schedule> : le schedule de l'auto-backup à mettre à jour ['daily', 'monthly', 'weekly', 'custom']\n
            \t- <custom_cron> : le schedule personnalisé à mettre à jour de l'auto-backup, obligatoire si l'option custom a été séléctionnée\n
            \tSi l'argument n'a pas été saisi, le programme rentre en mode interactif et attend des entrées de l'utilisateur pour compléter custom_cron.
    """
    log("Info", f"Name of cron : \"{idcron}\"")
    log("Info", f"New cron schedule : \"{new_cron_schedule}\"")
    if new_cron_schedule == 'custom':
        if not custom_cron:  # custom_cron n'est pas donné en argument
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
            custom_cron = concatenate_custom_cron()  # le custom_cron est donc demandé en input interactif
            log("Info", "Chosen custom cron schedule is :", custom_cron)
        else:  # Cron schedule is not custom
            click.echo("L'argument custom_cron n'est pas au format '0-59:0-23:1-31:1-12:0-6'. Ne définissez pas l'option pour la définir interactivement.")
            log("Error", "Chosen custom cron schedule is :", custom_cron)
    else:
        log("Info", "Cron schedule is :", new_cron_schedule)
        custom_cron = translate_cron_schedule(new_cron_schedule)
        if custom_cron == False:  # translate_cron_schedule() error
            click.echo("L'argument cron_schedule ne correspond pas à {daily, monthly, weekly, custom}")
    log("Info", "Calling kdna.conf CRUD...")
    AutoBackupService().update_auto_backup(idcron, new_cron_schedule="", new_name="", new_date="", new_path="")  # Modifie kdna.conf
    log("Info", "Calling parser...")
    parseConfig()  # Lance le parseur


# Création de la commande list
@autobackup.command()
def list():
    """Commande pour lister les autobackups\n
    :return: Liste des autobackups : class: `str`\n
    :rtype: list"""
    table = tabulate(
        [[data for data in autobackup.values()] for autobackup in autobackups],
        ['id', 'frequency', 'name', 'timestamp', 'id_server', 'path'],
        tablefmt="grid"
    )
    click.echo(table)


# Création de la commande stop
@autobackup.command()
@click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nom du cron à stopper")
def stop(nameofcron):
    """Commande pour stopper une backup régulière\n
    :param nameofcron: -n le nom du cron à stopper\n
    :type nameofcron: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    click.echo(f"Stopped cron : \"{nameofcron}\"")


# Création de la commande list
@autobackup.command()
def list():
    """Commande pour lister les autobackups
    :return: Liste des autobackups : class: `str`\n
    :rtype: list"""
    autobackupService = AutoBackupService()
    autobackups = autobackupService.find_all()
    table = tabulate(
        [[data for data in autobackup.values()] for autobackup in autobackups],
        ['id', 'frequency', 'name', 'timestamp', 'id_server', 'path'],
        tablefmt="grid"
    )
    click.echo(table)
