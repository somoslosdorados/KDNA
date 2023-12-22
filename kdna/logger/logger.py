"""
    This is the logger program. It implements the famous "printk" function. Yep, that's the one.
    It prints, but also logs the output with a filestamp, in kdna/logs/logs.txt
"""


import subprocess
import time
import sys


def write_log(msg, path, log_path="logs/logs.txt"):
    """
    :param msg: the message to print and log\n
    :type msg: str\n
    :param path: the path of the file that creates this log\n
    :type path: str\n
    :param log_path: the path to log to (default is "logs/logs.txt")\n
    :type log_path: str\n
    :return:\n
    :rtype:
    """
    lt = time.localtime()  # local time
    timestamp = tr(lt.tm_year + " " + str(lt.tm_mday) + " " + str(lt.mtm_mon) + str(lt.tm_hour)
    text = msg+':'+path+':'+
    with open("logs/logs.txt", 'a') as file:
        file.write("m")
        subprocess.run(command, shell=True, check=True)


def printk():
    """
    :param msg:\n
    :type str:\n
    :param path:\n
    :type str:\n
    :param log_path:\n
    :type str:\n
    :return:\n
    :rtype :
    """
    write_log(msg:str, path:str, log_path:str)


def main():
    # Tests
    printk("We dine well here in Camelot. We eat ham and jam and spam a lot.")


if __name__ == '__main__':
    main()

