from util.utilities import print_message
from channels import Group
import json
import subprocess
from pyesgf.logon import LogonManager
from pyesgf.search import SearchConnection
from constants import ESGF_SEARCH_SUFFIX, ESGF_CREDENTIALS, NODE_HOSTNAMES
from util.utilities import print_debug, print_message
import os
from sh import tail


def dispatch(message, data, user):
    destination = data.get('destination')
    if destination == 'dataset_download':
        return dataset_download(message, data, user)
    else:
        print_message('unrecognised destination {}'.format(destination))
        return -1
    return -1


def dataset_download(message, data, user):
    print 'got a dataset_download request'
    username = data.get('params').get('openid_username')
    password = data.get('params').get('openid_password')
    search_string = data.get('params').get('search_string')
    nodes = data.get('params').get('nodes')
    data_type = data.get('params').get('data_type')
    data_name = data.get('params').get('data_name')
    if not username:
        print_message('No username given')
        return -1
    if not password:
        print_message('No password given')
        return -1
    if not search_string:
        print_message('No search_string given')
        return -1
    if not nodes:
        print_message('No nodes given')
        return -1
    if not data_type:
        print_message('No data_type given')
        return -1
    if not data_name:
        print_message('No data_name given')
        return -1

    lm = LogonManager()
    lm.logon_with_openid(username, password, bootstrap=True)
    if not lm.is_logged_on():
        print_message('User {user} is not logged in during download request'.format(user=user))
        return -1
    for node in nodes:
        try:
            path = os.path.abspath(os.path.dirname(__file__)) + '/../../'
            print '[+] searching {node} for {string}'.format(node=node, string=search_string)
            conn_string = 'http://{node}{suffix}'.format(node=node, suffix=ESGF_SEARCH_SUFFIX)
            conn = SearchConnection(conn_string, distrib=True)
            context = conn.new_context(**search_string)
            rs = context.search()
            print_message('got reply from {node}'.format(node=node))
            if len(rs) == 0:
                continue

            script_text = context.get_download_script()
            script_path = ''
            if data_type == 'observation':
                script_path = path + 'userdata/' + user + '/observations/' + data_name
            elif data_type == 'model':
                script_path = path + 'userdata/' + user + '/model_output/' + data_name

            script_name = '{path}/{name}_download_script.sh'.format(path=script_path, name=data_name)
            if not os.path.exists(script_path):
                print_message('creating directory {}'.format(script_path))
                os.makedirs(script_path)
            try:
                with open(script_name, 'w') as script:
                    script.write(script_text)
                    script.close()
            except Exception, e:
                print_debug(e)

            word_count_cmd = 'cat {script_name} | grep \\.nc.*http:// | wc -l'.format(path=script_path, script_name=script_name)
            print_message('running command {}'.format(word_count_cmd))
            p = subprocess.check_output(word_count_cmd, shell=True)
            number_of_downloads = int(p)
            percent_complete = 0
            number_complete = 0.0
            print_message('Number of .nc files to download: {}'.format(number_of_downloads))

            try:
                subprocess.call(['chmod', '+x', script_name])
                p = subprocess.Popen('{name} > output_status.txt 2>&1'.format(name=script_name),
                                     shell=True,
                                     cwd=script_path)
                for line in tail('-f', '{path}/output_status.txt'.format(path=script_path), _iter=True):
                    if 'saved' in line or 'Saving to' in line:
                        number_complete += 1
                        percent_complete = number_complete / number_of_downloads * 100
                        # print_message('percent complete: {}%'.format(percent_complete), 'ok')
                        update_message = {
                            'text': json.dumps({
                                'user': user,
                                'data_name': data_name,
                                'percent_complete': percent_complete,
                                'destination': 'esgf_download_status'
                            })
                        }
                        Group('active').send(update_message)
                    if percent_complete > 99:
                        print_message('Download complete', 'ok')
                        update_message = {
                            'text': json.dumps({
                                'user': user,
                                'data_name': data_name,
                                'percent_complete': 100.0,
                                'destination': 'esgf_download_status'
                            })
                        }
                        Group('active').send(update_message)
                        break
                out, err = p.communicate()
                print out, err
            except Exception, e:
                print_debug(e)
                return -1
            break

        except Exception as e:
            print_debug(e)
            return -1
    return 0