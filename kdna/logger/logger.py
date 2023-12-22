"""
    This is the logger program. It implements the famous "printk" function. Yep, that's the one.
    It prints, but also logs the output with a filestamp, in kdna/logs/logs.txt
"""


import os
import time


def get_path():
    """
    :return: returns the path of the .py file it is executed it.\n
    :rtype: str
    """
    return os.path.dirname(__file__) + '/' + os.path.basename(__file__)


def write_log(msg, path, log_path="logs/logs.txt"):
    """
    :param msg: the message to print and log\n
    :type msg: str\n
    :param log_path: the path to log to (default is "logs/logs.txt")\n
    :type log_path: str\n
    :return: returns file.write output (that is, number of characters written)\n
    :rtype: int
    """
    lt = time.localtime()  # local time
    timestamp = "on " + lt(lt.tm_year + " " + str(lt.tm_mon) + " " + str(lt.tm_mday) + " at " + str(lt.tm_hour) + "h " + str(lt.min) + "m " + str(lt.sec) + "s")
    # local time is formatted as follows : "on year month day at hour minute second"
    text = msg+':'+path+':'+timestamp+'\n'
    with open("logs/logs.txt", 'a') as file:
        res = file.write(text)
    return res


def printk(msg, log_path):
    """
    This function acts 'like' print, but also logs what you printed in the chosen logs file (default is logs/logs.txt").
    :param msg: the message to print and log\n
    :type msg: str\n
    :param log_path: the path to log to (default is "logs/logs.txt")\n
    :type log_path: str\n
    :return: returns file.write output (that is, number of characters written)\n
    :rtype: int
    """
    path = get_path()
    res = write_log(str(msg), path)
    print(msg)
    return res


def main():
    # Tests
    printk("We dine well here in Camelot. We eat ham and jam and spam a lot.")


if __name__ == '__main__':
    main()

