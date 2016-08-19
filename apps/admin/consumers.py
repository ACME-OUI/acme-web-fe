from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http
from util.utilities import print_message
from apps.run_manager import dispatcher as rm_dispatch
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
    # print_message("got message: {}".format(message['text']))
    # {   u'content': u'hello world!',
    #     u'destination': u'init',
    #     u'target_app': u'run_manager'}

    # Group('run_manager').send({'text': message['text']})
    # message.reply_channel.send({'text': message['text']})

    data = json.loads(message['text'])
    # pp.pprint(data)
    target_app = data.get('target_app')
    if not target_app:
        print_message("No target_app given")
        return
    if target_app == 'run_manager':
        rm_dispatch.dispatch(message, data, message.user.username)
    else:
        print_message('unrecognized target_app {}'.format(target_app))
        return


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
