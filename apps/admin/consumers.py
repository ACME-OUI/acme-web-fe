from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http
from util.utilities import print_message
from apps.run_manager import dispatcher as rm_dispatch
from apps.esgf import dispatcher as esgf_dispatch
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)


@channel_session
@channel_session_user_from_http
def ws_connect(message):
    user = message.user.username
    print_message("got new connection from {}".format(user))
    Group(user).add(message.reply_channel)
    Group('active').add(message.reply_channel)
    message.channel_session['room'] = 'run_manager'


@channel_session
@channel_session_user_from_http
def ws_receive(message):
    data = json.loads(message['text'])
    # user = message.user.username
    # if user is None:
    user = data.get('user')
    if user is None:
        user = message.user.username

    print_message('Got a request with data {data} from {user}'.format(data=data, user=user))
    target_app = data.get('target_app')
    return_code = 0
    if not target_app:
        print_message("No target_app given")
        return_code = -1
    if target_app == 'run_manager':
        return_code = rm_dispatch.dispatch(message, data, user)
    elif target_app == 'esgf':
        return_code = esgf_dispatch.dispatch(message, data, user)
    else:
        print_message('unrecognized target_app {}'.format(target_app))
        return_code = -1
    return_val = {
        'text': json.dumps({
            'return_code': return_code
        })
    }
    Group('active').send(return_val)


@channel_session
@channel_session_user_from_http
def ws_disconnect(message):
    print_message('User disconnected')
    Group('active').discard(message.reply_channel)
    # pp.pprint(dir(message))
    # pp.pprint(message.user)
    # user = message.user.username
    # print_message('{} disconnected'.format(user))
    # Group(user).discard(message.reply_channel)
