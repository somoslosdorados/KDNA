"""Main : Commande pour afficher le contenu d'un fichier"""
import click


def display(path):
    """display : Affiche le contenu d'un fichier"""
    try:
        with open(path, mode="r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError as exc:
        raise FileNotFoundError("Fichier non trouvé") from exc

    except PermissionError as exc:
        raise PermissionError("Oups, Pas les droits") from exc


@click.group()
def kdna():
    """kdna : Commande principale"""


@kdna.group()
def backup():
    """backup: Commande pour sauvegarder un fichier"""


@kdna.group()
def server():
    """server: Commande pour lancer le serveur"""


@kdna.group()
def autobackup():
    """backup: Commande pour mettre en place un daemon de sauvegarde"""


@backup.command()
@click.option('-t', '--namepath', nargs=2, help="entrer le nom "
                                                "et le chemin du fichier à sauvegarder")
def add(namepath):
    """add: Commande pour simuler l'ajout d'un fichier à la sauvegarde
        -t, --namepath: option pour entrer le nom et le chemin du fichier à sauvegarder"""
    name, path = namepath
    click.echo(f"Created backup \"{name}\":v1.1.2")
    click.echo("Contains :")
    click.echo(display(path))


@server.command()
@click.argument('name')
def set(name):
    """set: Commande pour sélectionner un serveur
        --name: option pour entrer le nom du serveur"""
    click.echo(f"Picked server : \"{name}\"")


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


def main():
    """main: Fonction principale"""
    kdna()


if __name__ == '__main__':
    main()
