


# utilise les args de la commande de pauline dans commands/autobackup.py ; si a besoin d'utiliser plus d'args, lui dire (quelle ajoute aux params d ela cmd)


import sys # ? needed ? We'll see
import subprocess # ? to start bash scripts to make crons and stuff


def argv_getter():
    """
    """
    # mettre dans un module de fonctions auxilliaires ?
    pass
    nameofcron = sys.argv[1]
    tag = sys.argv[2]
    schedule = sys.argv[3]  # pre-made dates at which cron crons
    custom_cron = sys.argv[4]  # dates at which cron crons
    if schedule ==
    return nameofcron, tag, schedule, cron_schedule
        

"""
VOICI DE LA DOC POUR FAIRE LES CRON :
man crontab

format de crontab -e :
    Minute (0 - 59)
    Hour (0 - 23)
    Day of month (1 - 31)
    Month (1 - 12)
    Day of week (0 - 6) (Sunday is 0 or 7)

idée : faire des scripts qui vont CRUD le cron.
Ces scripts sont lancés par les fonctions de ce fichier.
Ce fichier est lancé par une commande du CLI. (Ce fichier est appelé avec ses arguments, tels que nameofcron, ...)
Ce fichier transmet aux scripts ces arguments pour que le cron soit créé.
"""


def delay_reformatter(delay):
    """
    """
    # mettre dans un module de fonctions auxilliaires ?
    # récupère la date de l'appel de la commande de paupau et la formatte pour le cron.
    pass


def cron_igniter(nameofcron:str, tag:str, cron_schedule:str, custom_cron:str):
    """
    Starts a cron
    """
    pass
    command = "./cronstart.sh"
    subprocess.run(command, shell=True, check=True)
