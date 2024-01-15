from fabric import Connection
from kdna.logger.logger import log


class SSHClient:

    def __init__(self, credentials, key_path=None):
        split = credentials.split("@")
        self.host = split[1]
        self.user = split[0]
        self.connection = None
        self.key_path = key_path

    def connect(self):
        if self.connection is None:
            self.connection = Connection(
                host=self.host,
                user=self.user,
                connect_kwargs=self._get_connect_kwargs()
            )
        return self

    def _get_connect_kwargs(self):
        connect_kwargs = {}
        if self.key_path:
            connect_kwargs["key_filename"] = self.key_path
        return connect_kwargs

    def disconnect(self):
        if self.connection is not None:
            self.connection = None

    def status(self):
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
        try:
            with Connection(host=self.host, user=self.user) as conn:
                # Récupère le retour de la commande
                command_return = conn.run(command, hide=True)
                msg = "\n{0.stdout}"
                return msg.format(command_return)
        except Exception as e:
            print(f"Error sending command {command} to {self.host}: {e}")
            log("ERROR",
                f"Error sending command {command} to {self.host}: {e}")

    def run(self, command: str):
        return self.connection.run(command, warn=True)
