from fabric import Connection

class SSHClient:

  def __init__(self, host, user, key_path=None):
    self.host = host
    self.user = user
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
        ram_info = conn.run("free -h | grep 'Mem:'", hide=True).stdout.strip()
        system_info['ram_info'] = ram_info

        # Système d'exploitation
        os_info = conn.run("uname -a", hide=True).stdout.strip()
        system_info['os_info'] = os_info

        # Utilisation des ressources
        resource_usage = conn.run("top -bn1 | grep 'Cpu(s)'", hide=True).stdout.strip()
        system_info['resource_usage'] = resource_usage
    except Exception as e:
      print(f"Error getting system information on {self.host}: {e}")
    return system_info
