class AutoBackup:
    def __init__(self, id_backup: str,frequency: int, alias: str, timestamp: int, id_server: str, path: str  ):
        self.id_backup = id_backup
        self.frequency = frequency
        self.alias = alias
        self.timestamp = timestamp
        self.id_server = id_server
        self.path = path


    def __str__(self):
        return f"AutoBackup: {self.id_backup} {self.frequency} {self.alias} {self.timestamp} {self.id_server} {self.path}"

class ParseAutoBackup:
    def __init__(self, line: str):
        self.line = line

    def parse(self) -> AutoBackup:
        values = self.line.strip().split(', ')
        id_backup, frequency, alias, timestamp, id_server, path = values
        return AutoBackup(id_backup, frequency, alias, timestamp, id_server, path)