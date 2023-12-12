class Server:
    def __init__(self, id_server: str, credentials: str, port: int, alias: str):
        self.id_server = id_server
        self.credentials = credentials
        self.port = port
        self.alias = alias

    def __str__(self):
        return f"Server: {self.id_server} {self.credentials} {self.port} {self.alias}"


class ParseServer:
    def __init__(self, line: str):
        self.line = line

    def parse(self) -> Server:
        id_server, credentials, port, alias = self.line.strip().split(', ')
        return Server(id_server, credentials, port, alias)