import subprocess
import click
from kdna.logger.logger import log  # Logging ability import


def list_crontab():
    try:
        result = subprocess.run(
            'crontab -l 2>&1 |grep -Ev "^(#|n)"', shell=True, stdout=subprocess.PIPE)
        return result.stdout.decode('utf-8').split('\n')[:-1]
    except subprocess.CalledProcessError as e:
        log("ERROR", f"Error listing crontab: {e}")


def add_cron_job(command, schedule):
    try:
        subprocess.run(
            f'(crontab -l 2>&1 |grep -Ev "^(#|n)" ; echo "{schedule} {command}") |sort |uniq |crontab -', shell=True)
        log("SUCCESS", "Cron job added successfully.")
    except subprocess.CalledProcessError as e:
        log("ERROR", f"Error adding cron job: {e}")


def update_cron_job(command, new_schedule):
    try:
        delete_cron_job(command)
        add_cron_job(command, new_schedule)
        log("SUCCESS", "Cron job updated successfully.")
    except subprocess.CalledProcessError as e:
        log("ERROR", f"Error updating cron job: {e}")
        raise Exception(f"Error updating cron job: {e}")


def delete_cron_job(command):
    process_command = f'(crontab -l 2>&1 |grep -Ev " {command}$") |sort |uniq |crontab -'
    try:
        subprocess.run(
            process_command,
            shell=True)
        log("SUCCESS", "Cron job deleted successfully.")
    except subprocess.CalledProcessError as e:
        log("ERROR", f"Error deleting cron job: {e}")
        raise Exception(f"Error deleting cron job: {e}")


def get_custom_cron(sched_part_type: str, cond_inf: int, cond_sup: int):
    """Fonction qui récupère auprès de l'utilisateur une partie de la \n
    date du schedule de custom_cron pour autobackup (e.g. renvoie la minute de
    backup, ou l'heure, ...).\n
    :param sched_part_type: le type de la partie manquante de custom_cron à
    demander à l'utilisateur (e.g. 'Hour')\n
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
            raise Exception("Valeur incorrecte.")

    return schedule_part + ':'


def concatenate_custom_cron():
    custom_cron = get_custom_cron("Minute", 0, 59)
    custom_cron += get_custom_cron("Heure", 0, 23)
    custom_cron += get_custom_cron("Jour du mois", 1, 31)
    custom_cron += get_custom_cron("Mois", 1, 12)
    custom_cron += get_custom_cron("Jour de la semaine", 0, 6)
    return custom_cron[:-1]  # Suppression du ':' final


def validate_cron_schedule(custom_cron: str):
    schedule_list = custom_cron.split(':')
    if len(schedule_list) != 5:
        return False
    else:
        # Check that every part is made only of numbers
        for part in schedule_list:
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
