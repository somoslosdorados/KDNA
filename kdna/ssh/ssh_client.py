from fabric import Connection

from kdna.logger.logger import log


class SSHClient:
    """ssh class client module"""
    def __init__(self, credentials, key_path=None):
        split = credentials.split("@")
        self.host = split[1]
        self.user = split[0]
        self.connection = None
        self.key_path = key_path

    def connect(self):
        """
        Connects to the specified host using the provided user credentials.

        If a connection has not been established yet, this method creates a new connection
        using the given host and user credentials. The connection is established with the
        help of the `Connection` class, which is initialized with the host, user, and
        connection kwargs obtained from the `_get_connect_kwargs` method.

        :return: The established connection.
        :rtype: Connection
        """
        if self.connection is None:
            self.connection = Connection(
                host=self.host,
                user=self.user,
                connect_kwargs=self._get_connect_kwargs()
            )
        return self

    def _get_connect_kwargs(self):
        """
        Returns the keyword arguments required for establishing a connection.

        :return: A dictionary containing the connection keyword arguments.
        :rtype: dict
        """
        connect_kwargs = {}
        if self.key_path:
            connect_kwargs["key_filename"] = self.key_path
        return connect_kwargs

    def disconnect(self):
        """
        Disconnects the current connection.

        This method sets the connection attribute to None, effectively disconnecting from the
        current connection.

        :return: None
        """
        if self.connection is not None:
            self.connection = None

    def status(self):
        """
        Retrieves system information from a remote host.

        Returns:
            dict: A dictionary containing the following system information:
                - 'ram_info' (str): The amount of RAM available on the system.
                - 'os_info' (str): The operating system information.
                - 'resource_usage' (str): The CPU resource usage.

        Raises:
            Exception: If there is an error retrieving the system information.

        """
        system_info = {}
        try:
            with Connection(host=self.host, user=self.user) as conn:
                # Nombre de RAM
                ram_info = conn.run("free -h | grep 'Mem:'",
                                    hide=True).stdout.strip()
                system_info['ram_info'] = ram_info

        # Système d'exploitation
                os_info = conn.run("uname -a", hide=True).stdout.strip()
                system_info['os_info'] = os_info

        # Utilisation des ressources
                resource_usage = conn.run(
                    "top -bn1 | grep 'Cpu(s)'", hide=True).stdout.strip()
                system_info['resource_usage'] = resource_usage
        except Exception as e:
            print(f"Error getting system information on {self.host}: {e}")
            log("ERROR",
                f"Error getting system information on {self.host}: {e}")
        return system_info

    def sendCommand(self, command):
        """
        Sends a command to the remote host and returns the output.

        :param command: The command to be sent to the remote host.
        :type command: str
        :return: The output of the command execution.
        :rtype: str
        :raises Exception: If there is an error sending the command.
        """
        with Connection(host=self.host, user=self.user) as conn:
            # Récupère le retour de la commande
            command_return = conn.run(command, hide=True)
            msg = "\n{0.stdout}"
            return msg.format(command_return)

    def run(self, command: str):
        """
        Executes the given command on the remote connection.

        :param command: A string representing the command to be executed.
        :type command: str
        :return: The result of the command execution.
        :rtype: str
        :raises: Any exception raised by the underlying connection.

        This method executes the specified command on the remote connection using the `run`
         method of the connection object.
        The `warn` parameter is set to True, which means that a warning will be issued if the
         command execution fails.

        """
        return self.connection.run(command, warn=True)
