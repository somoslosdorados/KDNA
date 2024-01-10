"""
    This is the logger program. It implements the "log" function. 
    Logs the timestamp, the alert_level, the path from where the log is called and the message, in kdna/logs/logs.log
    Réalisé par : Sarah THEOULLE et Théo TCHILLINGUIRIAN
"""

import time


def write_log(alert_level, msg, path):
    """
    :param msg: the message to print and log\n
    :type msg: str\n
    :param log_path: the path to log to (default is "logs/logs.log")\n
    :type log_path: str\n
    :return: returns file.write output (that is, number of characters written)\n
    :rtype: int
    """
    timestamp = "on " + time.strftime("%Y-%m-%d") + " at " + time.strftime("%Hh %Mm %Ss")
    text = timestamp + "  " + alert_level + "  " + path + " : " + msg + "\n"
    with open("kdna/logs/logs.log", 'a') as file:
        res = file.write(text)
    return res


def log(alert_level, msg, path):
    """
    This function acts 'like' print, but also logs what you printed in the chosen logs file (default is logs/logs.txt").
    :param msg: the message to print and log\n
    :type msg: str\n
    :param log_path: the path to log to (default is "logs/logs.txt")\n
    :type log_path: str\n
    :return: returns file.write output (that is, number of characters written)\n
    :rtype: int
    """
    res = write_log(str(alert_level), str(msg), str(path))
    return res


def main():
    log("Warning","We dine well here in Camelot. We eat ham and jam and spam a lot.", "path")


if __name__ == '__main__':
   main()

