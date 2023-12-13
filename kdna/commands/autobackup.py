import click

@click.group(name='auto-backup')
def autobackup():
    """backup: Commande pour mettre en place un daemon de sauvegarde"""

@autobackup.command()
@click.option('-n', '--nameofcron', nargs=1, help="entrer le nom du cron")
@click.option('-t', '--tag', nargs=1, help="entrer le tag")
@click.argument('cron_schedule', type=click.Choice(['daily', 'monthly', 'weekly',
                                                    'custom']), required=True)
@click.argument('custom_cron', nargs=-1)
def schedule(nameofcron, tag, cron_schedule, custom_cron):
    """schedule: Commande pour prévoir une backup régulière
        --nameofcron: option pour entrer le nom du cron
        --tag: option pour saisir un tag pour le cron
        --schedule: option pour choisir le schedule du cron
        --custom-cron: option pour entrer un cron personnalisé"""
    click.echo(f"Name of cron : \"{nameofcron}\"")
    click.echo(f"Cron tag and schedule : \"{tag}\" \"{cron_schedule}\"")
    if cron_schedule == 'custom':
        click.echo(f"Custom cron : \"{custom_cron}\"")

@autobackup.command()
@click.option('-n', '--nameofcron', nargs=1, help="entrer le nom du cron à stopper")
def stop(nameofcron):
    """schedule: Commande pour stopper une backup régulière
        --nameofcron: option pour entrer le nom du cron à stopper"""
    click.echo(f"Stopped cron : \"{nameofcron}\"")