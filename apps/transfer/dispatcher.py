from util.utilities import print_message
from util.utilities import print_debug
from util.utilities import project_root
from util.utilities import timeformat
from poller.models import UserRuns
from web_fe.models import Notification
from run_manager.dispatcher import group_job_update
from subprocess import Popen, PIPE
from channels import Group
from time import sleep

import datetime
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
    source_dir = params.get('remote_dir')
    remote_file = params.get('remote_file')
    destination_dir = params.get('destination_dir')
    source_server = params.get('source_server', 'edison.nersc.gov')
    destination_server = params.get('destination_server', 'pcmdi11.llnl.gov')

    if not source_dir:
        source_dir = ''
    source_dir.replace('\n', ' ')
    source_dir.replace('&', ' ')
    source_dir = '/project/projectdirs/acme/{}'.format(source_dir.split(' ')[0])

    if not remote_file:
        print_message('No remote file for transfer')
        return HttpResponse(status=400)
    remote_file.replace('\n', ' ')
    remote_file.replace('&', ' ')
    remote_file = remote_file.split(' ')[0]
    source_dir = '{folder}/{file}'.format(folder=source_dir, file=remote_file)

    if not destination_dir:
        destination_dir = ''
    destination_dir.replace('\n', ' ')
    source_dir.replace('&', ' ')

    folder_id = uuid.uuid4().hex
    destination_dir = '/{user}/{uuid}'.format(user=user, uuid=folder_id)

    config = {
        'run_type': 'file_transfer',
        'run_name': remote_file,
        'user': user,
        'request_attr': json.dumps({
            'source_dir': source_dir,
            'source_server': source_server,
            'destination_server': destination_server,
            'destination_dir': destination_dir
        })
    }
    try:
        new_run = UserRuns.objects.create(
            status='new',
            config_options=json.dumps(config),
            user=user
        )
        new_run.save()
    except Exception as e:
        print_debug(e)
        print_message('error saving new run')
        return -1

    message = {
        'run_name': remote_file,
        'run_type': config.get('run_type'),
        'request_attr': config.get('request_attr'),
        'timestamp': datetime.datetime.now().strftime(timeformat)
    }
    try:
        note = Notification.objects.get(user=new_run.user)
        new_notification = json.dumps({
            'job_id': new_run.id,
            'run_type': config.get('run_type'),
            'optional_message': message,
            'status': 'new',
            'timestamp': datetime.datetime.now().strftime(timeformat)
        })
        note.notification_list += new_notification + ' -|- '
        note.save()
    except Exception, e:
        raise

    try:
        cmd = ['python',
               os.path.join(project_root(), 'scripts/acme_transfer.py'),
               '--source-endpoint',
               'b9d02196-6d04-11e5-ba46-22000b92c6ec',  # edison@nersc
               '--source-path',
               source_dir,
               '--destination-endpoint',
               'a49fff56-96b9-11e6-b0ab-22000b92c261',  # pcmdi11@llnl
               '--destination-path',
               destination_dir,
               '--config',
               os.path.join(project_root(), 'userdata/system/config.json')]
        print_message(
            'Starting data transfer\n'
            'source_dir: {source_dir}, destination_dir: {destination_dir}'.format(
                source_dir=source_dir,
                destination_dir=destination_dir))
        print_message(' '.join(cmd))
        p = Popen(cmd, stdout=PIPE)
        new_run.status = 'in_progress'
        new_run.save()

        group_job_update(
            new_run.id,
            new_run.user,
            new_run.status,
            optional_message=new_run.config_options,
            destination='set_run_status')

        done = False
        while not done:
            try:
                msg = p.stdout.readline()
                done = p.poll()
                update_message = {
                    'text': json.dumps({
                        'user': user,
                        'data_name': remote_file,
                        'message': msg,
                        'destination': 'data_manager_transfer'
                    })
                }
                group_job_update(
                    new_run.id,
                    new_run.user,
                    new_run.status,
                    optional_message=update_message,
                    destination='data_manager_transfer')
            except Exception as e:
                print_message('no update from the transfer')
                print_debug(e)
            else:
                print_message(msg)
            finally:
                sleep(1)
        new_run.status = 'complete'
        new_run.save()
        update_message = {
            'text': json.dumps({
                'user': user,
                'data_name': remote_file,
                'message': 'transfer complete',
                'destination': 'data_manager_transfer'
            })
        }
        group_job_update(
            new_run.id,
            new_run.user,
            new_run.status,
            optional_message=update_message,
            destination='set_run_status')
    except Exception as e:
        print_message('Error transfering file')
        print_debug(e)
        return -1

    return 0
