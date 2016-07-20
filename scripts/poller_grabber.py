import time
import requests
import json
import sys
import traceback


def grab_job():
    url = "http://localhost:8000/poller/update"
    request = {
        'request': 'next'
    }
    return requests.get(url, params=request).content

def print_debug(e):
    print '1', e.__doc__
    print '2', sys.exc_info()
    print '3', sys.exc_info()[0]
    print '4', sys.exc_info()[1]
    print '5', traceback.tb_lineno(sys.exc_info()[2])
    ex_type, ex, tb = sys.exc_info()
    print '6', traceback.print_tb(tb)

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_message(message, status='error'):
    if status == 'error':
        print colors.FAIL + '[-] ' + colors.ENDC + colors.BOLD + str(message) + colors.ENDC
    elif status == 'ok':
        print colors.OKGREEN+ '[+] ' + colors.ENDC + str(message)



if __name__ == "__main__":
    while True:
        try:
            print_message('Grabbing the next job', 'ok')
            job = grab_job()
            print_message('New job: {}'.format(job))
        except Exception as e:
            print_message('Error grabbing a job')
            print_debug(e)
        time.sleep(60)
