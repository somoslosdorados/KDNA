


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
