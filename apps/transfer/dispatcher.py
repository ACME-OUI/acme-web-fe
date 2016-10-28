from util.utilities import print_message
from util.utilities import print_debug
from util.utilities import project_root
from subprocess import Popen, PIPE
from channels import Group
from time import sleep

import json
import subprocess
import os
import uuid


def dispatch(message, data, user):
    destination = data.get('destination')
    if destination == 'transfer_file':
        return transfer_file(message, data, user)
    else:
        print_message('unrecognised destination {}'.format(destination))
        return -1
    return -1


def transfer_file(message, data, user):
    print_message('transfer_file request', 'ok')
    print_message(data, 'ok')
    try:
        params = data.get('data').get('params')
    except Exception as e:
        print_message('Unable to decode params: {}'.format(data))
        return -1
    else:
        if not params:
            print_message('No params given')
            return -1
    remote_dir = params.get('remote_dir')
    remote_file = params.get('remote_file')
    local_dir = params.get('local_dir')

    if not remote_dir:
        remote_dir = ''
    remote_dir.replace('\n', ' ')
    remote_dir.replace('&', ' ')
    remote_dir = '/project/projectdirs/acme/{}'.format(remote_dir.split(' ')[0])

    if not remote_file:
        print_message('No remote file for transfer')
        return HttpResponse(status=400)
    remote_file.replace('\n', ' ')
    remote_file.replace('&', ' ')
    remote_file = remote_file.split(' ')[0]
    remote_dir = remote_dir.split(' ')[0]
    remote_dir = '/project/projectdirs/acme/{folder}/{file}'.format(folder=remote_dir, file=remote_file)

    if not local_dir:
        local_dir = ''
    local_dir.replace('\n', ' ')
    remote_dir.replace('&', ' ')
    local_dir = '/export/baldwin32/file_transfers/{user}/{uuid}'.format(user=user, uuid=uuid.uuid4().hex)

    try:
        cmd = ['python',
               os.path.join(project_root(), 'scripts/acme_transfer.py'),
               '--source-endpoint',
               'b9d02196-6d04-11e5-ba46-22000b92c6ec',  # edison@nersc
               '--source-path',
               remote_dir,
               '--destination-endpoint',
               'a49fff56-96b9-11e6-b0ab-22000b92c261',  # pcmdi11@llnl
               '--destination-path',
               local_dir,
               '--config',
               os.path.join(project_root(), 'userdata/system/config.json')]
        print_message('Starting data transfer\n remote_dir: {remote_dir}, local_dir: {local_dir}'.format(remote_dir=remote_dir, local_dir=local_dir))
        print_message(' '.join(cmd))
        p = Popen(cmd, stdout=PIPE)
        update_message = {
            'text': json.dumps({
                'user': user,
                'transfer_name': remote_dir
                'message': 'transfer started',
                'destination': 'data_manager_transfer'
            })
        }
        Group('active').send(update_message)
        while True:
            try:
                msg = p.stdout.readline()
                update_message = {
                    'text': json.dumps({
                        'user': user,
                        'data_name': remote_file,
                        'message': msg,
                        'destination': 'data_manager_transfer'
                    })
                }
                Group('active').send(update_message)
            except Exception as e:
                print_message('no update from the transfer')
                print_debug(e)
            else:
                print_message(msg)
                if msg == 'progress 1/1':
                    print_message('file transfer complete', 'ok')
                    break
            finally:
                sleep(1)
        update_message = {
            'text': json.dumps({
                'user': user,
                'data_name': remote_file,
                'message': 'transfer complete',
                'destination': 'data_manager_transfer'
            })
        }
        Group('active').send(update_message)
    except Exception as e:
        print_message('Error transfering file')
        print_debug(e)
        return -1

    return 0
