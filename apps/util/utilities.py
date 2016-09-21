import sys
import traceback
import pprint
import os
import json
pp = pprint.PrettyPrinter(indent=4)


def get_client_ip(request):
    """see: http://stackoverflow.com/a/4581997"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


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
        print(colors.FAIL + '[-] ' + colors.ENDC + colors.BOLD + str(message) + colors.ENDC)
    elif status == 'ok':
        print(colors.OKGREEN + '[+] ' + colors.ENDC + str(message))


# see: http://code.activestate.com/recipes/577879-create-a-nested-dictionary-from-oswalk/
def get_directory_structure(rootdir):
    """
    Creates a nested dictionary that represents the folder structure of rootdir
    """
    dir = {}
    rootdir = rootdir.rstrip(os.sep)
    start = rootdir.rfind(os.sep) + 1
    for path, dirs, files in os.walk(rootdir, followlinks=True):
        folders = path[start:].split(os.sep)
        subdir = dict.fromkeys(files)
        parent = reduce(dict.get, folders[:-1], dir)
        parent[folders[-1]] = subdir
    return dir


def check_params(params, check_list):
    '''
    Checks the parameters agains a list of expected values
    '''
    output = {}
    for item in check_list:
        if item in params:
            output[item] = params[item]
        else:
            print_message('Parameter not given: {}'.format(item))
            output[item] = None
    for item in params:
        if item not in check_list:
            print_message('Unrecognized parameter: {}'.format(item))
    return output


def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except Exception as e:
        return False
    return True
