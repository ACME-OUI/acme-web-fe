from util.utilities import print_message
from channels import Group

import json


# An empty dict subclass, to allow me to call poller views directly
# without needing to make an http request
class mydict(dict):
    pass


def dispatch(message, data, user):
    destination = data.get('destination')
    if destination == 'init':
        return init(message, data, user)
        # group_job_update(9999, 'testest', 'rockin it')
    elif destination == 'status_update':
        return status_update(message, data, user)
    elif destination == 'send_to_group':
        return send_to_group(data, user)
    else:
        print_message('unrecognized destination function {}'.format(destination))
        return -1


def init(message, data, user):
    message.reply_channel.send({'text': 'connection initialized to run manager'})
    return 0


def status_update(message, data, user):
    return -1


def send_to_group(data, group):
    Group(group).send(data)
    return 0


def group_job_update(job_id, user, status, optional_message=None, destination='set_run_status'):
    text = {
        'destination': destination,
        'job_id': job_id,
        'user': user,
        'status': status,
        'optional_message': optional_message
    }
    message = {'text': json.dumps(text)}
    Group('active').send(message)

    text['destination'] = 'notification'
    message = {'text': json.dumps(text)}
    Group('active').send(message)
