"""
Module to connect to a remote server using SSH and Paramiko.
"""

import os
import sys
import getpass
import paramiko
from paramiko import SSHClient, AutoAddPolicy


def is_key(key_path):
    """
    Check if a file is a valid SSH key.
    """
    with open(key_path, "r", encoding="utf-8") as file:
        first_line = file.readline()
    return "PRIVATE KEY" in first_line


def list_ssh_config_hosts():
    """
    List all hosts in the SSH config file.
    """
    config_file = os.path.expanduser("~/.ssh/config")
    if not os.path.exists(config_file):
        return []
    with open(config_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    hosts = [line.split()[1] for line in lines if line.startswith("Host ")]
    return hosts


def get_ssh_config_info(host):
    """
    Get the hostname and username from the SSH config file.
    """
    config = paramiko.SSHConfig()
    user_config_file = os.path.expanduser("~/.ssh/config")
    if os.path.exists(user_config_file):
        with open(user_config_file, encoding="utf-8") as f:
            config.parse(f)
    cfg = {"hostname": host, "username": None}
    user_config = config.lookup(host)
    if "hostname" in user_config:
        cfg["hostname"] = user_config["hostname"]
    if "user" in user_config:
        cfg["username"] = user_config["user"]
    return cfg


def connect_with_keys(client, hostname, username):
    """
    Connect to a remote server using SSH keys.
    """
    key_folder = os.path.expanduser("~/.ssh")
    for key_filename in os.listdir(key_folder):
        key_path = os.path.join(key_folder, key_filename)
        if not is_key(key_path):
            print(f"Skipping {key_filename} because it is not a key")
            continue
        try:
            print(f"Trying key {key_filename}")
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(hostname, username=username, key_filename=key_path)
            return True
        except Exception as e:
            print(f"Failed with key {key_filename}: {e}")
    return False


def main():
    """
    Main function.
    """
    use_known_host = (
        input("Use known server from SSH config? (yes/no): ").strip().lower() == "yes"
    )

    if use_known_host:
        hosts = list_ssh_config_hosts()
        print("Available hosts:")
        for i, host in enumerate(hosts):
            print(f"{i + 1}. {host}")
        choice = int(input("Select a host number: ")) - 1
        config_info = get_ssh_config_info(hosts[choice])
    else:
        config_info = {
            "hostname": input("Enter hostname: "),
            "username": input("Enter username: "),
        }

    client = SSHClient()
    connected = connect_with_keys(
        client, config_info["hostname"], config_info["username"]
    )

    if not connected:
        password = getpass.getpass("SSH key failed. Enter password: ")
        try:
            client.load_system_host_keys()
            client.set_missing_host_key_policy(AutoAddPolicy())
            client.connect(
                config_info["hostname"],
                username=config_info["username"],
                password=password,
            )
        except Exception as e:
            print(f"Failed to connect with password: {e}")
            sys.exit(1)

    _, stdout, _ = client.exec_command("ls kdna")
    if stdout.channel.recv_exit_status() == 0:
        _, stdout, _ = client.exec_command("tree kdna")
        print(stdout.read().decode())
    else:
        print("kdna folder does not exist on the remote server")

    client.close()


if __name__ == "__main__":
    main()
