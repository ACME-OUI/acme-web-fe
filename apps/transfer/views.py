from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from util.utilities import print_message
from util.utilities import print_debug
from util.utilities import project_root
from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue, Empty
from time import sleep

import paramiko
import json
import uuid
import os


@login_required
def view_remote_directory(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        print_message('Unable to decode request.body: {}'.format(request.body))
        return HttpResponse(status=400)

    user = str(request.user)
    remote_dir = data.get('remote_dir')
    if not remote_dir:
        remote_dir = ''
    remote_dir.replace('\n', ' ')
    remote_dir.replace('&', ' ')
    remote_dir = '/project/projectdirs/acme/{}'.format(remote_dir.split(' ')[0])

    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        print_message('No username or password in request.body, using session data')
        try:
            username = request.session.get('nersc_username')
            password = request.session.get('nersc_password')
        except Exception as e:
            print_message('could not extract username from session')
            return HttpResponse(status=400)
    if not username or not password:
        print_message('No username or password')
        return HttpResponse(status=400)
    try:
        print_message('connecting', 'ok')
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect('edison.nersc.gov',
                       port=22,
                       username=username,
                       password=password)
        print_message('connected!', 'ok')
    except Exception as e:
        print_message('Error connecting to publication server')
        print_debug(e)
        return HttpResponse(status=500)

    print_message('Looking up remote folder {}'.format(remote_dir))
    command = "python ~/scripts/get_dir_contents.py {}".format(remote_dir)
    try:
        stdin, stdout, stderr = client.exec_command(command)
    except Exception as e:
        print_debug(e)
        print_message('Error executing command {}'.format(command))
        return HttpResponse(status=500)
    response = {
        'error': stderr.read(),
        'out': stdout.read()
    }
    return HttpResponse(json.dumps(response))


@login_required
def nersc_credential_check(request):
    try:
        u = request.session.get('nersc_username')
        p = request.session.get('nersc_password')
        if u and p:
            return HttpResponse()
    except Exception as e:
        return HttpResponse(status=400)
    else:
        return HttpResponse(status=400)


@login_required
def nersc_login(request):
    try:
        data = json.loads(request.body)
    except Exception as e:
        print_message('Unable to decode request.body: {}'.format(request.body))
        return HttpResponse(status=400)

    user = str(request.user)
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        print_message('No username or password')
        return HttpResponse(status=400)

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect('edison.nersc.gov',
                       port=22,
                       username=username,
                       password=password)
    except Exception as e:
        print_message('Error connecting to nersc via ssh')
        print_debug(e)
        return HttpResponse(status=500)
    else:
        print_message('saving credentials to session')
        request.session['nersc_username'] = username
        request.session['nersc_password'] = password
        print_message('session user={}, pass={}'.format(request.session.get('nersc_username'), request.session.get('nersc_password')))
    print_message('login successful')
    return HttpResponse()
