import pytest
from kdna.tags import tags 
from fabric import Connection
from kdna.parsing import parser
from kdna.ssh.ssh_client import SSHClient

@pytest.mark.skip(reason="Not implemented yet")
@pytest.fixture
def connexion_instance():
    parser.parseConfig()
    list_servers = parser.listServers
    found = False
    for server_i in list_servers:
        if server_i.id_server == "test":
            found = True
            connection_instance = SSHClient(server_i.credentials,server_i.path)
            connection_instance.connect()
            connection_instance.connection.run("mkdir -p ./kdna/.test/test.tar.gz")
            break
    if not found:
        raise FileNotFoundError("Server not found")
    yield
    connection_instance.connection.run("rm -rf ./kdna/.test")


def test_add_tags(connexion_instance):
    tags.add_tags(connexion_instance.connection, ".test", "tag", "test.tar.gz")
    assert tags.tag_exists(connexion_instance.connection, ".test", "tag")