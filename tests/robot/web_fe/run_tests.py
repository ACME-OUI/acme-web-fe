# ''' A runner script for all acme-web-fe tests
#
#     If no arguments are given, this script will run the tests against a local
#         server running at port 8000
#
#     If you would like to test it against another server, give the address as an argument '''
# import os
# import sys
# from subprocess import Popen, PIPE
#
#
# server = 'localhost:8000'
#
# if len(sys.argv) > 1:
#     server = sys.argv[1]
#
#
# def run_tests(test):
#     process = Popen(
#         ['pybot', '--outputdir', test, '--variable', 'SERVER:' + server, test], stdout=PIPE)
#     (out, err) = process.communicate()
#     exit_code = process.wait()
#     print out
#
#
# if __name__ == '__main__':
#     for test in next(os.walk(os.getcwd()))[1]:
#         print 'Running test', test
#         run_tests(test)
