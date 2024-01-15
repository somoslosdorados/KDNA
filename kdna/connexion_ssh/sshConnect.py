from fabric import Connection

from kdna.logger.logger import log


class SSHClient:

    def __init__(self, name, ip) -> None:
        self.user = name
        self.serverIP = ip
        self.SSHInstance = None

    def getSSHparameter(self):
        """
        Returns the SSH parameter for connecting to the server.

        :return: A string representing the SSH parameter in the format 'user@serverIP'.
        :rtype: str
        """
        return self.user + '@' + self.serverIP

    def connect(self):
        """
        Connects to the SSH server using the provided SSH parameters.

        :return: The SSH connection instance if successful, otherwise None.
        :rtype: Connection or None
        :raises: Exception if an error occurs during the connection process.

        This method attempts to establish a connection to the SSH server using the SSH parameters obtained from the
        `getSSHParameter` method. If the connection is successful, it returns the SSH connection instance. If an error
        occurs during the connection process, an exception is raised and an error message is printed and logged.

        """
        try:
            self.SSHInstance = Connection(self.getSSHParameter())
        except:
            print("An error as occured on connection")
            log("ERROR", "An error as occured on connection")
            return None

    def closeConnection(self):
        """
        Closes the SSH connection.

        This method closes the SSH connection by calling the close() method of the SSHInstance object.

        :return: None
        :rtype: None
        :raises: None
        """
        try:
            self.SSHInstance.close()
        except:
            print("An error as occured while closing ssh instance")
            log("ERROR", "An error as occured while closing ssh instance")
            return None

    def sendCommand(self, command):
        """
        Sends a command to the SSH instance and returns the result.

        :param command: The command to be sent to the SSH instance.
        :type command: str
        :return: The result of the command execution.
        :rtype: str or None
        :raises: Exception if an error occurs during command execution.

        This method sends the specified command to the SSH instance and returns the result of the command execution.
        If an error occurs during command execution, an exception is raised and logged.

        Example usage:
            result = sendCommand("ls -l")
        """
        try:
            result = self.SSHInstance.run(command, hide=True)
            msg = "\n{0.stdout}"
        except:
            print("An error as occured: " + "\n{0.stderr}")
            log("ERROR", "An error as occured: " + "\n{0.stderr}")
            return None
