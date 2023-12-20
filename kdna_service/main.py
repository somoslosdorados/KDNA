"""
    This program is started by the kdna daemon. It generates a log every x seconds to demonstrate the python service.

    This program takes one command-line argument x, an integer interpreted as the time in seconds between logs.
    
    This program writes logs.
"""


import subprocess
import time
import sys


def main():
    """
    Main script function.

    :raises [ValueError]: [this error may occur during type conversion]
    :raises [IndexError]: [this error may occur during sys.argv list traversal]
    :return: [no errors or exceptions]
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

