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
import paramiko


def dispatch(message, data, user):
    destination = data.get('destination')
    if destination == 'transfer_file':
        return transfer_file(message, data, user)
    elif destination == 'publish_file':
        return publish_file(message, data, user)
    else:
        print_message('unrecognised destination {}'.format(destination))
        return -1
    return -1


def publish_file(message, data, user):
    destination = '/export/baldwin32/file_transfer/' + uuid.uuid4().hex
    retval = transfer_file(
        message,
        data,
        user,
        override_destination=destination)

    try:
        params = data.get('data').get('params')
    except Exception as e:
        print_message('Unable to decode params: {}'.format(data))
        return -1
    else:
        if not params:
            print_message('No params given')
            return -1

    username = params.get('username')
    password = params.get('password')

    if not username or not password:
        print_message('No username or password')
        return -1
    try:
        print_message('connecting to publication server', 'ok')
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect('pcmdi11.llnl.gov',
                       port=22,
                       username=username,
                       password=password)
        print_message('connected!', 'ok')
    except Exception as e:
        print_message('Error connecting to publication server')
        print_debug(e)
        return -1

    pub_name = params.get('pub_name')
    pub_org = params.get('pub_org')
    pub_firstname = params.get('pub_firstname')
    pub_lastname = params.get('pub_lastname')
    pub_desc = params.get('pub_desc')
    facets = params.get('pub_facets')
    remote_file = params.get('remote_file')

    submission_config = {
        'metadata': [
            {
                'name': 'name',
                'value': pub_name
            },
            {
                'name': 'organization',
                'value': pub_org,
            },
            {
                'name': 'firstname',
                'value': pub_firstname,
            },
            {
                'name': 'lastname',
                'value': pub_lastname,
            },
            {
                'name': 'description',
                'value': pub_desc,
            },
            {
                'name': 'datanode',
                'value': 'pcmdi11.llnl.gov'
            }
        ],
        'facets': [{
            'name': 'project',
            'value': 'ACME'
        },{
            'name': 'data_type',
            'value': 'h0'
        },{
            'name': 'experiment',
            'value': 'b1850c5_m1a'
        },{
            'name': 'versionnum',
            'value': 'v0_1'
        },{
            'name': 'realm',
            'value': 'atm'
        },{
            'name': 'regridding',
            'value': 'ne30_g16'
        },{
            'name': 'range',
            'value': 'all'
        }],
        'scan': {
            'options': '',
            'path': destination
        },
        'publish': {
            'options': {
                'files': 'all'
            },
            'files': []
        }
    }
    command = "python ~/publication/publish.py {}".format(json.dumps(submission_config).replace("\"", "\\\""))
    print_message(command)

    config = {
        'run_type': 'file_publish',
        'run_name': remote_file,
        'user': user,
        'request_attr': json.dumps(submission_config)
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
        print_message('Error creating new notification')
        print_debug(e)
        return -1

    group_job_update(
        new_run.id,
        new_run.user,
        new_run.status,
        optional_message=new_run.config_options,
        destination='set_run_status')

    try:
        stdin, stdout, stderr = client.exec_command(command, get_pty=True)
    except Exception as e:
        print_debug(e)
        print_message('Error executing command {}'.format(command))
        client.close()
        return -1

    new_run.status = 'in_progress'
    new_run.save()
    message = {
        'run_name': remote_file,
        'run_type': config.get('run_type'),
        'request_attr': config.get('request_attr'),
        'timestamp': datetime.datetime.now().strftime(timeformat),
        'error': 'stdout',
        'out': 'stderr'
    }
    try:
        note = Notification.objects.get(user=new_run.user)
        new_notification = json.dumps({
            'job_id': new_run.id,
            'run_type': config.get('run_type'),
            'optional_message': message,
            'status': 'in_progress',
            'timestamp': datetime.datetime.now().strftime(timeformat)
        })
        note.notification_list += new_notification + ' -|- '
        note.save()
    except Exception, e:
        raise
    group_job_update(
        new_run.id,
        new_run.user,
        new_run.status,
        optional_message=new_notification,
        destination='set_run_status')

    out = stdout.read()
    err = stderr.read()
    print_message(out, 'ok')
    print_message(err)

    if 'successfully' in out:
        try:
            note = Notification.objects.get(user=new_run.user)
            new_notification = json.dumps({
                'job_id': new_run.id,
                'run_type': config.get('run_type'),
                'optional_message': message,
                'status': 'complete',
                'timestamp': datetime.datetime.now().strftime(timeformat)
            })
            note.notification_list += new_notification + ' -|- '
            note.save()
        except Exception, e:
            raise
        group_job_update(
            new_run.id,
            new_run.user,
            new_run.status,
            optional_message=new_notification,
            destination='set_run_status')
    else:
        try:
            note = Notification.objects.get(user=new_run.user)
            new_notification = json.dumps({
                'job_id': new_run.id,
                'run_type': config.get('run_type'),
                'optional_message': message,
                'status': 'error',
                'timestamp': datetime.datetime.now().strftime(timeformat)
            })
            note.notification_list += new_notification + ' -|- '
            note.save()
        except Exception, e:
            raise
        group_job_update(
            new_run.id,
            new_run.user,
            new_run.status,
            optional_message=new_notification,
            destination='set_run_status')


def transfer_file(message, data, user, override_destination=False):
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
    data_type = params.get('data_type', 'diagnostic')

    if destination_server == 'pcmdi11.llnl.gov':
        destination_endpoint = 'a49fff56-96b9-11e6-b0ab-22000b92c261'
        print_message('transfering to pcmdi11', 'ok')
    elif destination_server == 'aims4.llnl.gov':
        destination_endpoint = '43d64772-a82e-11e5-99d3-22000b96db58'
        print_message('transfering to aims4', 'ok')
    else:
        destination_endpoint = 'a49fff56-96b9-11e6-b0ab-22000b92c261'
        print_message('transfering to pcmdi11', 'ok')

    if not source_dir:
        source_dir = ''
    source_dir.replace('\n', ' ')
    source_dir.replace('&', ' ')
    source_dir = '/project/projectdirs/acme/{}'.format(source_dir.split(' ')[0])

    if not remote_file:
        print_message('No remote file for transfer')
        return -1
    remote_file.replace('\n', ' ')
    remote_file.replace('&', ' ')
    remote_file = remote_file.split(' ')[0]
    source_dir = '{folder}/{file}'.format(folder=source_dir, file=remote_file)

    if not destination_dir:
        destination_dir = ''
    destination_dir.replace('\n', ' ')
    source_dir.replace('&', ' ')

    if override_destination:
        destination_path = override_destination
    else:
        destination_path = '{project_root}/userdata/{user}/'.format(
            project_root=project_root(),
            user=user)
        if data_type == 'diagnostic':
            destination_path += 'diagnostic_output/'
        elif data_type == 'model':
            destination_path += 'model_output/'
        elif data_type == 'observation':
            destination_path += 'observations/'
        else:
            print_message('Invalid data_type {}'.format(data_type))
            return -1

        if destination_dir == 'new':
            destination_dir = destination_path + remote_file.split('.')[0] + '/' + remote_file
        else:
            destination_dir = destination_path + destination_dir + '/' + remote_file

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
    group_job_update(
        new_run.id,
        new_run.user,
        new_run.status,
        optional_message=new_run.config_options,
        destination='set_run_status')

    try:
        cmd = ['python',
               os.path.join(project_root(), 'scripts/acme_transfer.py'),
               '--source-endpoint',
               'b9d02196-6d04-11e5-ba46-22000b92c6ec',  # edison@nersc
               '--source-path',
               source_dir,
               '--destination-endpoint',
               destination_endpoint,  # pcmdi11@llnl
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

        done = 2
        while done != 0:
            try:
                msg = p.stdout.readline()
                done = p.poll()
                print 'done: ' + str(done)
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
        print_message("file transfer complete", 'ok')
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
