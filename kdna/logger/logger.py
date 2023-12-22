"""
    This is the logger program. It implements the famous "printk" function. Yep, that's the one.
    It prints, but also logs the output with a filestamp, in kdna/logs/logs.txt
"""


import subprocess
import time
import sys


def write_log(msg, path, log_path="logs/logs.txt"):
    """
    :param msg: le message to print and log\n
    :type msg: str\n
    :param path:\n
    :type path: str\n
    :param log_path:\n
    :type log_path: str\n
    :return:\n
    :rtype:
    """
    with open("logs/logs.txt", 'w'):
        subprocess.run(command, shell=True, check=True)
        time.sleep(x)


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

def main():
    """
    Main function.

    Inputs:
        No parameters.
        This function takes one command-line argument x, an integer interpreted as the time in seconds between logs.
    Ouputs:
        0 -> no errors or exceptions.
        1 -> Generic error 'Exception'.
        2 -> 'ValueError' (e.g. during type conversion).
        3 -> 'IndexError' (e.g. during sys.argv list traversal).
    """

    try:
        x = int(sys.argv[1])  # This catches the first argument (if it exists) after main.py in the command-line. Pattern example : python3 main.py arg1 arg2 arg3 ...

    except ValueError as err:
        print(f"An error occurred during argument conversion, please input an integer. The error is as follows: {err} - dated $(date)")
        return 2
    
    except IndexError as err:
        print(f"An error occurred during argument list traversal, this program requires an integer argument to define log delay. The error is as follows: {err} - dated $(date)")
        return 3
    # The catched exception messages appear in `journalctl -u kdnad` and in `systemctl status kdnad.service`

    else:  # Entered only if try was successful and no exceptions raised.
        i=0
        while 1:
            i+=1
            command = 'echo "Hi ! This log is dated $(date) - log number {} of session - and will log every {} seconds." >> /root/kdna_service/logs.txt'.format(i, x)
            subprocess.run(command, shell=True, check=True)
            time.sleep(x)  # New log every x seconds.
        return 0

    return 1  # Catches general exceptions / errors


if __name__ == '__main__':
    main()

