import os
import pytest

from kdna.conf_utils.utils import Utils

config_file = "tests/data/test_conf_utils.txt"

def test_find_servers_index():
    lines = [
        '[server]\n',
        '[auto-backup]'
    ]
    index = Utils.find_servers_index(lines)
    assert index == 0
    
def test_find_auto_backups_index():
    lines = [
        '[server]\n',
        '[auto-backup]'
    ]
    index = Utils.find_auto_backups_index(lines)
    assert index == 1

def test_find_section1():
    lines = [
        '[server]\n',
        '[auto-backup]'
    ]
    index = Utils.find_section(lines, "[server]")
    assert index == 0
    
def test_find_section2():
    lines = [
        '[server]\n',
        '[auto-backup]'
    ]
    index = Utils.find_section(lines, "[auto-backup]")
    assert index == 1

def test_delete_line():
    lines = [
        "[server]\n",
        "1",
        "2",
        "3",
        "4",
    ]
    lines2 = [
        "[server]\n",
        "1",
        "2",
        "4",
    ]
    Utils.delete_line(lines, 3)
    assert lines == lines2
    
def test_read_file_lines():
    lines = [
        '[server]\n',
        '[auto-backup]'
    ]
    lines2 = Utils.read_file_lines(config_file)
    print(lines2)
    assert lines == lines2

@pytest.mark.skip(reason="Not implemented yet")
def test_write_file_lines():
    pass
    
@pytest.mark.skip(reason="Not implemented yet")
def test_read_all():
    pass

@pytest.mark.skip(reason="Not implemented yet")
def test_initialize_config_file():
    pass
