import os
import pytest

from kdna.conf_utils.utils import Utils

config_file = "tests/data/test_conf_utils.txt"

def test_find_servers_index():
    lines = [
        '[servers]\n',
        '[auto-backups]'
    ]
    index = Utils.find_servers_index(lines)
    assert index == 0
    
def test_find_auto_backups_index():
    lines = [
        '[servers]\n',
        '[auto-backups]'
    ]
    index = Utils.find_auto_backups_index(lines)
    assert index == 1

def test_find_section1():
    lines = [
        '[servers]\n',
        '[auto-backups]'
    ]
    index = Utils.find_section(lines, "[servers]")
    assert index == 0
    
def test_find_section2():
    lines = [
        '[servers]\n',
        '[auto-backups]'
    ]
    index = Utils.find_section(lines, "[auto-backups]")
    assert index == 1

def test_delete_line():
    lines = [
        "[servers]\n",
        "1",
        "2",
        "3",
        "4",
    ]
    lines2 = [
        "[servers]\n",
        "1",
        "2",
        "4",
    ]
    Utils.delete_line(lines, 3)
    assert lines == lines2
    
def test_read_file_lines():
    lines = [
        '[servers]\n',
        '[auto-backups]'
    ]
    lines2 = Utils.read_file_lines(config_file)
    assert lines == lines2

@pytest.mark.skip(reason="Not implemented yet")
def test_write_file_lines():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_initialize_config_file():
    pass
