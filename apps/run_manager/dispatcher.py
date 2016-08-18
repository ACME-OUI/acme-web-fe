# {   u'content': u'hello world!',
#     u'destination': u'init',
#     u'target_app': u'run_manager'}
# from poller.views import update as poller_update
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
        init(message, data, user)
        # group_job_update(9999, 'testest', 'rockin it')
    elif destination == 'status_update':
        status_update(message, data, user)
    elif destination == 'send_to_group':
        send_to_group(data, user)
    else:
        print_message('unrecognized destination function {}'.format(destination))


def init(message, data, user):
    message.reply_channel.send({'text': 'connection initialized to run manager'})

# def status_update(message, data, user):
#     params = mydict()
#     params.GET = {'user': user, 'request': 'all'}
#     params.method = 'GET'
#
#     try:
#         r = poller_update(params)
#         # r = requests.get(url, params={'user': user, 'request': 'all'})
#         if(r.status_code != 200):
#             print_message('Poller error with params {}'.format(params))
#         message.reply_channel.send(r.content)
#     except Exception as e:
#         print_message("Error getting run status with url: {}".format(url))
#         print_debug(e)

def send_to_group(data, group):
    Group(group).send(data)

def group_job_update(job_id, user, status):
    message = {
        'text': json.dumps({
            'destination': 'set_run_status',
            'job_id': job_id,
            'user': user,
            'status': status
        })
    }
    Group('active').send(message)
