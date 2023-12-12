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


def main():
    """main: Fonction principale"""
    kdna()

if __name__ == '__main__':
    main()
