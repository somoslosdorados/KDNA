from dependency_injector import containers, providers
from kdna.ssh.ssh_client import SSHClient

class Container(containers.DeclarativeContainer):
    ssh_client = providers.Factory(
        SSHClient,
        host="example.com", port=22, username="username", password="password"
    )