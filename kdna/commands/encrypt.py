"""
This module contains the commands for encryption managing in kdna.

:author: DURAT Mathias
:email: mathias.durat01@etu.umontpellier.fr
:date: 2023-12-20
"""
import click
from kdna.encrypt.encrypt import generate_key


@click.group()
def encrypt():
    """Command to enable/deactivate encryption and generate encryption key"""


@encrypt.command(name='key-gen')
@click.option('-p', '--path', required=False, default="", help="entrer le path du fichier si vous voulez")
def keygen(path):
    """Command to generate encryption key
    :param path: option to specify the path of the key"""
    if path == "":
        output_path = generate_key()
    else:
        try:
            output_path = generate_key(path)
        except Exception:
            click.echo("Path must lead to a file not a directory")
            return
    click.echo(f"Key generated at {output_path}")


@encrypt.command(name='activate')
def activate():
    """Command to enable encryption"""
    click.echo("Encryption activated")


@encrypt.command(name='deactivate')
def deactivate():
    """Command to disable encryption"""
    click.echo("Encryption deactivated")
