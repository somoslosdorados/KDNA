from kdna.ssh.ssh_client import SSHClient
import injector

def configure_container(binder):
    binder.bind(SSHClient, to=SSHClient("example.com", 22, "username", "password"))

container = injector.Injector()
container.binder.install(configure_container)