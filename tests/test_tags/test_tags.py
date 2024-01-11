import pytest
from kdna.tags import tags 
from fabric import Connection

@pytest.fixture
def connexion_instance():
    c =  Connection("debian12.local")
    if c.is_connected:
        return c

def test_add_tags():
    path_to_conf_tag = "./kdna/project/tags.conf"
    tags.add_tags(connexion_instance, "project", "tag", "save", True)
    assert connexion_instance.exists(path_to_conf_tag)
    tags.get_tag_conf(path_to_conf_tag, connexion_instance)
    try:
        with open('tags.conf', "r") as tag_file:
            tag_lines = tag_file.readlines()
        tag_lines.pop(0)
    except PermissionError:
        raise PermissionError("Erreur de permission: read sur tags.conf")
    found = False
    for line in tag_lines:
        tag_file_couple = line.split(", ")
        if ("tag" == tag_file_couple[0]):
            found = True
    assert found

def test_delete_tags():
    path_to_conf_tag = "./kdna/project/tags.conf"
    tags.delete_tags(connexion_instance, "project", "tag", True)
    assert connexion_instance.exists(path_to_conf_tag)
    tags.get_tag_conf(path_to_conf_tag, connexion_instance)
    try:
        with open('tags.conf', "r") as tag_file:
            tag_lines = tag_file.readlines()
        tag_lines.pop(0)
    except PermissionError:
        raise PermissionError("Erreur de permission: read sur tags.conf")
    found = False
    for line in tag_lines:
        tag_file_couple = line.split(", ")
        if ("tag" == tag_file_couple[0]):
            found = True
    assert not found

def test_update_tags():
    path_to_conf_tag = "./kdna/project/tags.conf"
    tags.update_tags(connexion_instance, "project", "newtag", "tag", "save", True)
    assert connexion_instance.exists(path_to_conf_tag)
    tags.get_tag_conf(path_to_conf_tag, connexion_instance)
    try:
        with open('tags.conf', "r") as tag_file:
            tag_lines = tag_file.readlines()
        tag_lines.pop(0)
    except PermissionError:
        raise PermissionError("Erreur de permission: read sur tags.conf")
    found = False
    for line in tag_lines:
        tag_file_couple = line.split(", ")
        if ("tag" == tag_file_couple[0]):
            found = True
    assert not found
    found = False
    for line in tag_lines:
        tag_file_couple = line.split(", ")
        if ("newtag" == tag_file_couple[0]):
            found = True
    assert found

def test_read_tags():
    tags.read_tags(connexion_instance, "project")
    assert True
    
