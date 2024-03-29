class Server:
    """Classe definissant un serveur
    id_server: str
    credentials: str
    port: int
    alias: str
    """

    def __init__(self, id_server: str, credentials: str, path: str, port: int, alias: str,
                 encrypt: bool):
        """Constructeur de la classe"""
        self.id_server = id_server
        self.credentials = credentials
        self.path = path
        self.port = port
        self.alias = alias
        self.encrypt = encrypt

    def __str__(self):
        """Methode d'affichage de la classe"""
        return (f"Server: {self.id_server} {self.credentials} {self.path} {self.port} {self.alias} "
                f"{self.encrypt}")


def parseServer(line):
    """Methode permettant de parser un serveur"""
    values = line.strip().split(', ')
    id_server, credentials, path, port, encrypt, alias = values
    return Server(id_server, credentials, path, port, encrypt, alias)
