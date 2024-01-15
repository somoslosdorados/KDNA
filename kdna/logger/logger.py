"""
    This is the logger program. It implements the "log" function. 
    Logs the timestamp, the alert_level, the path from where the log is called and the message,
    in ~/.kdna/kdna.log
    
    Notice: if you need to log anything, import this module and use the log function provided
    (logs its input).

    Authors: Sarah THEOULLE, Théo TCHILINGUIRIAN
"""

import inspect
import os
import time


def log(alert_level: str, msg: str):
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
    # Absolute path of the file that is calling the log function:
    caller_frame = inspect.stack()[1]
    # Get the filename and path from the frame
    caller_filename = caller_frame.filename
    path = os.path.abspath(caller_filename)
    timestamp = "on " + time.strftime("%Y-%m-%d") + " at " + time.strftime("%Hh %Mm %Ss")
    text = timestamp + " : " + alert_level + " : " + path + " : " + msg + "\n"
    with open(os.path.expanduser('~') + "/.kdna/kdna.log", 'a', encoding='utf-8') as file:
        res = file.write(text)
    return res
