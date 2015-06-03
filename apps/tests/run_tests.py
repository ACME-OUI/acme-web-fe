''' A runner script for all acme-web-fe tests

    If no arguments are given, this script will run the tests against a local
        server running at port 8000

    If you would like to test it against another server, give the address as an argument '''
import os
import sys
from subprocess import Popen, PIPE

try:
    import SeleniumLibrary
except ImportError:
    print 'SeleniumLibrary module missing'
    sys.exit(1)

server = 'http://localhost:8000'

if len(sys.argv) > 1:
    server = sys.argv[1]


def start_selenium():
    log = open('semenium_log.txt', 'w')
    SeleniumLibrary.start_selenium_server(log)


def run_tests(test):
    process = Popen(
        ['pybot', '--variable', 'SERVER:' + server, test], stdout=PIPE)
    (out, err) = process.communicate()
    exit_code = process.wait()

if __name__ == '__main__':
    for test in next(os.walk(os.getcwd()))[1]:
        run_tests(test)
