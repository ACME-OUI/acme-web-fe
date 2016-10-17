from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from util.utilities import print_message
from util.utilities import print_debug

import paramiko
import json


@login_required
def view_remote_directory(request):
    data = json.loads(request.body)
    user = str(request.user)
    remote_dir = data.get('remote_dir')
    if not remote_dir:
        remote_dir = ''
    remote_dir = '/project/projectdirs/acme/{}'.format(remote_dir.split(' ')[0])
    keypath = 'somekeypath'
    keypass = 'apassword'

    k = paramiko.RSAKey.from_private_key_file(keypath, password=keypass)
    c = paramiko.SSHClient()
    # c.load_system_host_keys()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print "connecting"
    c.connect( hostname="edison.nersc.gov", username="sbaldwin", pkey=k )
    print "connected"
    command = "python /scripts/get_dir_contents.py {}".format(remote_dir)
    stdin, stdout, stderr = c.exec_command(command)
    directory = {}
    out = stdout.read()
    err = stderr.read()
    return HttpResponse(json.dumps({
        'out': out,
        'error': err
    }))
