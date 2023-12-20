import click


# Creation du groupe de commande autobackup
@click.group(name='auto-backup')
def autobackup():
    """Commande pour mettre en place un daemon de sauvegarde"""


def get_type_cron(cron):
    for char in cron:
        print("caractere"+char) #test pour voir les caractère parcourus
        if char == ':':
            return ':'
        elif char == '-':
            return '-'
        else:
            return -1


def is_valid_cron(cron):
    print(get_type_cron(cron)) #test pour voir à quoi ressemble la variable cron
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


# Création des commandes du groupe autobackup

# Création de la commande schedule
@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron")
@click.option('-n', '--nameofcron', nargs=1, required=True, help="entrer le nom du cron")
@click.option('-t', '--tag', nargs=1, required=True, help="entrer le tag")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly',
                                                    'custom']), required=True)
@click.argument('custom_cron', nargs=-1)
@click.option('-d', '--date', nargs=1, required=True, help="entrer la date de la première backup [ xxxx-xx-xx ]")
@click.option('-s', '--server', nargs=1, required=True, help="entrer l'id du serveur")
@click.option('-p', '--path', nargs=1, required=True, help="entrer le chemin de la backup")
def schedule(idcron, nameofcron, tag, cron_schedule, custom_cron, date, server, path):
    """Commande pour prévoir une backup régulière\n
    :param idcron: -i l'id du cron\n
    :type idcron: str\n
    :param nameofcron: -n le nom du cron\n
    :type nameofcron: str\n
    :param tag: -t le tag du cron\n
    :type tag: str\n
    :param cron_schedule: le schedule de l'auto-backup ['daily', 'monthly', 'weekly', 'custom']\n
    :type cron_schedule: str\n
    :param custom_cron: le schedule personnalisé de l'auto-backup\n
    :type custom_cron: str, optional\n
    :param date: -d [ xxxx-xx-xx ] la date de la première backup\n
    :type date: str\n
    :param server: -s l'id du serveur\n
    :type server: str\n
    :param path: -p le chemin de la backup\n
    :type path: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    click.echo(f"Name of cron : \"{nameofcron}\"")
    click.echo(f"Cron tag and schedule : \"{tag}\" \"{cron_schedule}\"")
    if cron_schedule == 'custom':
        if not custom_cron:
            click.echo("L'argument custom_cron doit être suivi d'un schedule de cron personnalisé.")
        else:
            print("custom"+str(custom_cron)) #test
            print(is_valid_cron(str(custom_cron)))
    else:
        print(cron_schedule)


# Création de la commande delete
@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron à supprimer")
def delete(idcron):
    """Commande pour supprimer une backup régulière\n
    :param idcron: -n l'id du cron à supprimer\n
    :type idcron: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
    click.echo(f"Deleted cron : \"{idcron}\"")


@autobackup.command()
@click.option('-i', '--idcron', nargs=1, required=True, help="entrer l'id du cron à mettre à jour")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly',
                                                    'custom']), required=False)
@click.argument('custom_cron', nargs=-1, required=False)
@click.option('-d', '--date', nargs=1, required=False,
              help="entrer la nouvelle date de la première backup [ xxxx-xx-xx ]")
@click.option('-p', '--path', nargs=1, required=False, help="entrer le chemin de la nouvelle backup")
def update(idcron, tag, cron_schedule, custom_cron):
    """Commande pour mettre à jour une backup régulière\n
    :param idcron: -i l'id du cron\n
    :type idcron: str\n
    :param cron_schedule: le schedule de l'auto-backup ['daily', 'monthly', 'weekly', 'custom']\n
    :type cron_schedule: str\n
    :param custom_cron: le schedule personnalisé de l'auto-backup\n
    :type custom_cron: str, optional\n
    :param date: -d [ xxxx-xx-xx ] la date de la première backup\n
    :type date: str\n
    :param path: -p le chemin de la backup\n
    :type path: str\n
    :return: un message de confirmation ou d'erreur\n
    :rtype: str"""
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
    click.echo(f"List of autobackups : \n...\n...")
