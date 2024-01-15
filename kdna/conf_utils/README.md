
# Description

This module provides utility functions for managing configuration files in the context of the KDNA project.

## Méthodes

1. ### `initialize_config_file()`
    Initializes the `kdna.conf` configuration file. It creates the `.kdna` folder in the user directory if it doesn't exist, then creates the configuration file with the `[servers]` and `[auto-backups]` sections.

    ```python
    Utils.initialize_config_file()
    ```

2. ### `get_config_file_path()`
    Returns the full path to the kdna.conf configuration file.

    ```
    path = Utils.get_config_file_path()
    ```

3. ### `read_all()`
    Displays all configurations present in the kdna.conf file.

    ```
    Utils.read_all()
    ```

4. ### `read_file_lines(filename: str)`
    Returns all the lines in the file as a list.

    ```
    lines = Utils.read_file_lines("example.conf")
    ```

5. ### `write_file_lines(filename: str, lines: List[str])`
    Writes lines to the specified file.

    ```
    Utils.write_file_lines("example.conf", ["line1", "line2"])
    ```

6. ### `find_section(lines: List[str], pattern: str)`
    Returns the index of the first line containing the specified pattern.

    ```
    index = Utils.find_section(lines, "[servers]")
    ```

7. ### `find_auto_backups_index(lines: List[str])`
    This method returns the index of the [auto-backups] section in the file.

    ```
    index = Utils.find_auto_backups_index(lines)
    ```

8. ### `find_servers_index(lines: List[str])`
    This method returns 
    This method returns the index of the [servers] section in the file.
    ```
    index = Utils.find_servers_index(lines)
    ```
9. ### `delete_line(lines: List[str], line_to_delete: int)`
    This method deletes a specific line from the file.
    ```
    Utils.delete_line(lines, 3)
    ```