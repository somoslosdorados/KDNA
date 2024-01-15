import pytest
from kdna.tags import tags 
from kdna.ssh.ssh_client import SSHClient

@pytest.fixture
def connexion_instance():
    connection_instance = SSHClient("dtetu@localhost","/home/dtetu/.ssh/id_ed25519_python")
    connection_instance.connect()
    connection_instance.connection.run("mkdir -p ./kdna/.test")
    connection_instance.connection.run("touch ./kdna/.test/test.tar.gz")
    yield
    connection_instance.connection.run("rm -rf ./kdna/.test")

def test_add_tags(connexion_instance):
    tags.add_tags(connexion_instance.connection, "test", "test", ".test/test.tar.gz")
    assert tags.tag_exists(connexion_instance.connection, "test", "test") == True
