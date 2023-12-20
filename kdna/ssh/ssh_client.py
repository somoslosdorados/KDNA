class SSHClient:
    def __init__(self, host, port, username, password):
        # Initialisation de la connexion SSH ici
        self.host = host
        self.port = port
        self.username = username
        self.password = password