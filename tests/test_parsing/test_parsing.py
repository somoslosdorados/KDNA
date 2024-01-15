import os
from kdna.parsing.parser import line_is_header, parseConfig, listServers, listAutoBackups, kdna_path
import io


def test_parse_config(mocker, capsys):
    # Test case 1: Test with valid configuration file
    # Create a temporary configuration file with valid content
    with open("kdna.conf", "w") as f:
        f.write("[servers]\n")
        f.write("server1, credential, path, port, encrypt, alias\n")
        f.write("server2, credential, path, port, encrypt, alias\n")
        f.write("[auto-backups]\n")
        f.write("backup1, credential, path, port, encrypt, alias\n")
        f.write("backup2, credential, path, port, encrypt, alias\n")

    # Call the parseConfig function
    mocker.patch("kdna.parsing.parser.kdna_path", "")
    parseConfig()

    listNameServers = []
    listAutoBackupsName = []
    for server in listServers:
        listNameServers.append(server.id_server)

    for autobackup in listAutoBackups:
        listAutoBackupsName.append(autobackup.id_backup)

    # Assert that the parsed data is correct
    assert listNameServers == ["server1", "server2"]
    assert listAutoBackupsName == ["backup1", "backup2"]

    # Test case 2: Test with invalid header
    # Create a temporary configuration file with an unknown header
    with open("kdna.conf", "w") as f:
        f.write("[unknown-header]\n")
        f.write("line1\n")
        f.write("line2\n")

    # Call the parseConfig function
    # Create an instance of StringIO to capture the output

    parseConfig()
    captured_output = capsys.readouterr()

    # Assert that an error message is printed
    assert "Unknown header: unknown-header" in captured_output.out

    # Clean up the temporary configuration file
    os.remove("kdna.conf")


def test_line_is_header():
    # Test case 1: Valid header
    line = "[servers]\n"
    assert line_is_header(line) == "servers"

    # Test case 2: Invalid header (missing closing bracket)
    line = "[invalid-header\n"
    assert line_is_header(line) is None
