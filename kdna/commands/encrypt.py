"""
This module contains the commands for encryption managing in kdna.

:author: DURAT Mathias
:email: mathias.durat01@etu.umontpellier.fr
:date: 2023-12-20
"""
import click
from kdna.conf_utils.server import Server


@click.group()
def encrypt():
    """Command to enable/deactivate encryption and generate encryption key"""


@encrypt.command(name='key-gen')
@click.option('--path', is_flag=True, default=False)
def keygen(path):
    """Command to generate encryption key
    :param path: option to specify the path of the key"""
    if path:
        click.echo(f"Key stored to {path}")
    click.echo(f"Key generated")


@encrypt.command(name='activate')
def activate():
    """Command to enable encryption"""
    click.echo(f"Encryption activated")


@encrypt.command()
def deactivate():
    """Command to disable encryption"""
    click.echo(f"Encryption deactivated")
