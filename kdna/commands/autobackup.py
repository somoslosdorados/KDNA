"""
Groupe de commandes auto-backup qui permet de gérer les auto-backups (backups régulières)
schedule : Commande pour prévoir une auto-backup
delete : Commande pour supprimer une auto-backup
update : Commande pour mettre à jour une auto-backup
stop : Commande pour stopper une auto-backup
list : Commande pour lister les auto-backups
"""

import click


# Creation du groupe de commande autobackup
@click.group(name='auto-backup')
def autobackup():
    """Commande pour mettre en place un daemon de sauvegarde"""


def get_custom_cron(sched_part_type: str, cond_inf: int, cond_sup: int):
    """Fonction qui récupère auprès de l'utilisateur un morceau de custom_cron.\n
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
            print(
                "Minute (0 - 59)\nHeure (0 - 23)\nJour du mois (1 - 31)\nMois (1 - 12)\nJour de la semaine (0 - 6) (dimanche est 0)\nNe rien entrer pour ne pas préciser.")
        elif schedule_part == '' or cond_inf <= int(schedule_part) <= cond_sup:
            incorrect = False
        else:
            print("Entrée invalide, réessayez S.V.P")

    return schedule_part + ':'


def concatenate_custom_cron():
    """
    """
    custom_cron = get_custom_cron("Minute", 0, 59)
    custom_cron += get_custom_cron("Heure", 0, 23)
    custom_cron += get_custom_cron("Jour du mois", 0, 31)
    custom_cron += get_custom_cron("Mois", 1, 12)
    custom_cron += get_custom_cron("Jour de la semaine", 0, 6)
    return custom_cron[:-1]  # Suppression du ':' final


# Création des commandes du groupe autobackup

# Création de la commande schedule
@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron")
@click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nom du cron")
@click.option('-t', '--tag', nargs=1, required=True, help="entrer le tag")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly', 'custom']), required=True)
@click.argument('custom_cron', nargs=-1)
@click.option('-d', '--date', nargs=1, required=True, help="entrer la date de la première backup [ xxxx-xx-xx ]")
@click.option('-s', '--server', nargs=1, required=True, help="entrer l'id du serveur")
@click.option('-p', '--path', nargs=1, required=True, help="entrer le chemin de la backup")
def schedule(idcron, nameofcron, tag, cron_schedule, custom_cron, date, server, path):
    click.echo(f"Name of cron : \"{nameofcron}\"")
    click.echo(f"Cron tag and schedule : \"{tag}\" \"{cron_schedule}\"")
    if cron_schedule == 'custom':
        if not custom_cron:  # custom_cron n'est pas donné en argument
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
            custom_cron = concatenate_custom_cron()  # le custom_cron est donc demandé en input interactif
            print("Custom cron schedule is :", custom_cron)
        else:
            print("Custom cron schedule is :", custom_cron[0])
    else:
        print("Cron schedule is :", cron_schedule, "(not custom)")


# Création de la commande delete
@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron à supprimer")
def delete(idcron):
    click.echo(f"Deleted cron : \"{idcron}\"")


@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron à mettre à jour")
@click.option('-t', '--tag', nargs=1, required=False, help="entrer le tag du cron à mettre à jour")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly',
                                                    'custom']), required=False)
@click.argument('custom_cron', nargs=-1, required=False)
@click.option('-d', '--date', nargs=1, required=False,
              help="entrer la nouvelle date de la première backup [ xxxx-xx-xx ]")
@click.option('-p', '--path', nargs=1, required=False, help="entrer le chemin de la nouvelle backup")
def update(idcron, tag, cron_schedule, custom_cron, date, path):
    click.echo(f"Name of cron : \"{idcron}\"")
    click.echo(f"Cron tag and schedule : \"{tag}\" \"{cron_schedule}\"")
    if cron_schedule == 'custom':
        if not custom_cron:
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
        else:
            click.echo(f"Custom cron : \"{custom_cron}\"")


# Création de la commande stop
@autobackup.command()
@click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nom du cron à stopper")
def stop(nameofcron):
    click.echo(f"Stopped cron : \"{nameofcron}\"")


# Création de la commande list
@autobackup.command()
def list():
    click.echo(f"List of autobackups : \n...\n...")
