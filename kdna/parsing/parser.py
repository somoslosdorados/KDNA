from kdna.logger.logger import log
from kdna.parsing.server import parseServer
from kdna.parsing.autobackup import parse
import os

lines = {}
listServers = []
listAutoBackups = []

kdna_path = os.path.join(os.path.expanduser('~'), '.kdna')


def parseConfig():
    """
    Parse le fichier de configuration
    Repère les headers et les lignes associées
    Applique le bon parser en fonction du header si il est présent dans le dictionnaire parsers_strategy
    """
    line = ""
    header = ""
    previous_header = ""

    parsers_strategy = {
        "servers": cb_server_parser,
        "auto-backups": cb_autobackup_parser
    }
    path_to_config = os.path.join(kdna_path, "kdna.conf")

    with open(path_to_config, "r") as f:
        line = f.readline()
        while line:
            header = line_is_header(line)
            if header:
                previous_header = header
                lines[header] = []
            else:
                header = previous_header
                lines[header].append(line)
            line = f.readline()

    for header in lines.keys():
        if header in parsers_strategy:
            parser = parsers_strategy[header]
            for line in lines[header]:
                parsed = parser(line)
                #Store in right list (servers, autobackups, etc.)
                if header == "servers":
                    listServers.append(parsed)
                elif header == "auto-backups":
                    listAutoBackups.append(parsed)
        else:
            print(f"Unknown header: {header}")
            log("error", f"Unknown header: {header}")


def line_is_header(line: str) -> str:
    """
    Verifie si la ligne est un header
    """
    if line.startswith("[") and (line.endswith("]\n") or line.endswith("]")) :
        return line[1:-2]
    return None


def cb_server_parser(line: str):
    '''
    Callback permettant de parser un serveur'''
    return parseServer(line)


def cb_autobackup_parser(line: str):
    '''
    Callback permettant de parser un backup automatique'''
    return parse(line)
