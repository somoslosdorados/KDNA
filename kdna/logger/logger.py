"""
    This is the logger program. It implements the "log" function. 
    Logs the timestamp, the alert_level, the path from where the log is called and the message, in kdna/logs/logs.log
    
    Notice: if you need to log anything, import this module and use the log function provided (logs its input).

    Authors: Sarah THEOULLE, Théo TCHILINGUIRIAN
"""

import os
import time


def log(alert_level:str, msg:str):
    """
    This function writes the given input to the logs file (log file is kdna/logs/kdna.log").\n
    :param alert_level: the importance or type of the logged message\n
    :type msg: str\n
    :param msg: the message to print and log\n
    :type msg: str\n
    :param log_path: the path to log to\n
    :type log_path: str\n
    :return: returns file.write output (that is, number of characters written)\n
    :rtype: int
    """
    # Create /var/log/kdna/ directory if it doesn't exist. Should be done at kdna app installation.
    if not os.path.exists(os.path.join('kdna/logs')):
        os.mkdir('/kdna/logs')
    # Absolute path of the file that is calling the log function:
    path = os.path.abspath(__file__)
    timestamp = "on " + time.strftime("%Y-%m-%d") + " at " + time.strftime("%Hh %Mm %Ss")
    text = timestamp + " : " + alert_level + " : " + path + " : " + msg + "\n"
    with open("kdna/logs/kdna.log", 'a') as file:
        res = file.write(text)
    return res

def log_backup(alert_level:str, msg:str):
    """
    This function writes the given input to the logs file when it's about an autobackup(log file is /var/log/kdna/kdna.log").\n
    :param alert_level: the importance or type of the logged message\n
    :type msg: str\n
    :param msg: the message to print and log\n
    :type msg: str\n
    :param log_path: the path to log to \n
    :type log_path: str\n
    :return: returns file.write output (that is, number of characters written)\n
    :rtype: int
    """
    if not os.path.exists(os.path.join('/var/log/kdna')):
        os.mkdir('/var/log/kdna/')
    # Absolute path of the file that is calling the log function:
    path = os.path.abspath(__file__)
    timestamp = "on " + time.strftime("%Y-%m-%d") + " at " + time.strftime("%Hh %Mm %Ss")
    text = timestamp + " : " + alert_level + " : " + path + " : " + msg + "\n"
    with open("/var/log/kdna/kdna.log", 'a') as file:
        res = file.write(text)
    return res

