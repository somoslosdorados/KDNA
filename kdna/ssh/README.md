# SSHClient

## Overview

The `SSHClient` is a simple Python class that provides an interface for connecting to a remote server over SSH using the [Fabric](https://www.fabfile.org/) library.

## Usage

To use the `SSHClient`, follow these steps:

1. Import the class:

    ```python
    from ssh_client import SSHClient
    ```

2. Create an instance of `SSHClient`:

    ```python
    credentials = "username@hostname"
    key_path = "/path/to/private/key.pem"  # Optional
    ssh_client = SSHClient(credentials, key_path)
    ```

   Replace `username` with the SSH username and `hostname` with the IP address or hostname of the remote server. The `key_path` parameter is optional and can be used to specify the path to a private key for authentication.

3. Connect to the remote server:

    ```python
    ssh_client.connect()
    ```

4. Disconnect when done:

    ```python
    ssh_client.disconnect()
    ```

## Class Methods

### `__init__(credentials: str, key_path: Optional[str] = None)`

Constructor for the `SSHClient` class.

- `credentials`: A string in the format "username@hostname" representing the SSH credentials.
- `key_path`: Optional. The path to the private key for authentication.

### `connect() -> SSHClient`

Establishes an SSH connection to the remote server.

### `disconnect()`

Closes the SSH connection.

### `status() -> Dict[str, str]`

Retrieves information about the remote server's system status, including RAM, OS details, and resource usage.

### `sendCommand(command: str) -> str`

Sends a command to the remote server and returns the output.

## Example

```python
from ssh_client import SSHClient

# Initialize SSHClient
credentials = "username@hostname"
key_path = "/path/to/private/key.pem"
ssh_client = SSHClient(credentials, key_path)

# Connect to the remote server
ssh_client.connect()

# Get system status
status_info = ssh_client.status()
print(status_info)

# Send a command
command_result = ssh_client.sendCommand("ls -l")
print(command_result)

# Disconnect
ssh_client.disconnect()
