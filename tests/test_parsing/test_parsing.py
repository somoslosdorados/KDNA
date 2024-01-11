import os
from kdna.parsing.parser import line_is_header, parseConfig
import io
import pytest
import shutil

def test_parseConfig():
    # Test case 1: Test with valid configuration file
    # Create a temporary configuration file with valid content
    with open("temp_config.conf", "w") as f:
        f.write("servers\n")
        f.write("server1\n")
        f.write("server2\n")
        f.write("auto-backups\n")
        f.write("backup1\n")
        f.write("backup2\n")

    # Call the parseConfig function
    listServers = []
    listAutoBackups = []
    parseConfig()

    # Assert that the parsed data is correct
    assert listServers == ["server1", "server2"]
    assert listAutoBackups == ["backup1", "backup2"]

    # Test case 2: Test with invalid header
    # Create a temporary configuration file with an unknown header
    with open("temp_config.conf", "w") as f:
        f.write("unknown-header\n")
        f.write("line1\n")
        f.write("line2\n")

    # Call the parseConfig function
    # Create an instance of StringIO to capture the output
    captured_output = io.StringIO()

    parseConfig()

    # Assert that an error message is printed
    assert "Unknown header: unknown-header" in captured_output.getvalue()

    # Clean up the temporary configuration file
    os.remove("temp_config.conf")




def test_line_is_header():
    # Test case 1: Valid header
    line = "[servers]\n"
    assert line_is_header(line) == "servers"

    # Test case 2: Invalid header (missing closing bracket)
    line = "[invalid-header\n"
    assert line_is_header(line) is None
