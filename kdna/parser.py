from kdna.parsing.server import ParseServer
from kdna.parsing.autobackup import ParseAutoBackup

lines = {}

def parseConfig():
    line = ""
    header = ""
    previous_header = ""

    parsers_strategy = {
        "server": cb_server_parser,
        "auto-backup": cb_autobackup_parser
    }

    with open("kdna.conf", "r") as f:
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
                print(parser(line).parse())
        else:
            print(f"Unknown header: {header}")


def line_is_header(line: str) -> str:
    """
    Checks if a line is a header so it matches the regex [to-return]
    """
    if line.startswith("[") and line.endswith("]\n"):
        return line[1:-2]
    return None


def cb_server_parser(line: str):
    return ParseServer(line)

def cb_autobackup_parser(line: str):
    return ParseAutoBackup(line)
