import pytest
from kdna.tags import tags 
from unittest import mock
from fabric import Connection
from unittest.mock import MagicMock
from fabric import Connection
from unittest.mock import patch

@pytest.fixture
def connexion_instance():
    with mock.patch('fabric.Connection') as mock_connection:
        mock_connection.return_value = MagicMock(spec=Connection)
        yield mock_connection

def test_add_tags(connexion_instance):
    tags.add_tags(connexion_instance.connection, "test", "test", ".test/test.tar.gz")
    
def test_delete_tags(connexion_instance):
    with patch.object(tags, 'get_tag_conf') as mock_get_tag_conf:
        mock_get_tag_conf.return_value = {'test': 'test'}
        tags.delete_tags(connexion_instance.connection, "test", "test")
        with pytest.raises(KeyError):
            tags.delete_tags(connexion_instance.connection, "test", "test qui n'existe pas")

def test_update_tags(connexion_instance):
    with patch.object(tags, 'get_tag_conf') as mock_get_tag_conf:
        mock_get_tag_conf.return_value = {'test': 'test'}
        tags.update_tags(connexion_instance.connection, "test", "test", "test2")
        with pytest.raises(KeyError):
            tags.update_tags(connexion_instance.connection, "test", "test2", "test2")

def test_generate_tag_name(connexion_instance):
    assert tags.generate_tag_name(connexion_instance.connection, "test", "test") != None

def test_tag_exists(connexion_instance):
    with patch.object(tags, 'get_tag_conf') as mock_get_tag_conf:
        mock_get_tag_conf.return_value = {'test': 'test'}
        assert tags.tag_exists(connexion_instance.connection, "test", "test") == True
        assert tags.tag_exists(connexion_instance.connection, "test", "test2") == False

def test_get_file_name_by_tag(connexion_instance):
    with patch.object(tags, 'get_tag_conf') as mock_get_tag_conf:
        mock_get_tag_conf.return_value = {'test': 'testfile'}
        assert tags.get_file_name_by_tag(connexion_instance.connection, "test", "test") == 'testfile'
        with pytest.raises(FileNotFoundError):
            tags.get_file_name_by_tag(connexion_instance.connection, "test", "test2")
