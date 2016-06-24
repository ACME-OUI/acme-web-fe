import VeloAPI
from django.http import HttpResponse
import json
from web_fe.models import Credential
from util.utilities import print_debug
import requests
import os
from django.contrib.auth.decorators import login_required


@login_required
def delete(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data['name']

            cred = Credential.objects.get(
                site_user_name=request.user, service="velo")

            data = {
                'command': 'delete',
                'velo_user': cred.service_user_name,
                'velo_pass': cred.password,
                'resource': name
            }
            if velo_request(data) >= 0:
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=500)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def get_folder(request):
    if request.method == 'POST':
        folder = json.loads(request.body)['file']
        try:
            cred = Credential.objects.get(
                site_user_name=request.user, service='velo')
            if folder == '/User Documents/':
                folder += cred.service_user_name
            request = {
                'velo_user': cred.service_user_name,
                'velo_pass': cred.password,
                'command': 'get_folder',
                'folder': folder
            }
            out = velo_request(request)
            out = out.split(',')
            out.insert(0, folder)
            out = [o for o in out if o != '']
            return HttpResponse(json.dumps(out))

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def get_file(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            filename = data['filename']
            remote_file_path = os.path.join(data['path'], filename)
            cred = Credential.objects.get(
                site_user_name=request.user, service='velo')

            local_path = os.path.join(os.getcwd(), 'userdata', cred.service_user_name)
            # Create the local directories if they dont exist
            remote_path = remote_file_path.split('/')
            prefix = local_path[
                :local_path.index(cred.service_user_name) + len(cred.service_user_name)] + '/'
            if not os.path.isdir(prefix):
                os.makedirs(prefix)

            for i in range(remote_path.index(cred.service_user_name) + 1, len(remote_path) - 1):
                if not os.path.isdir(prefix + remote_path[i]):
                    prefix += remote_path[i] + '/'
                    os.makedirs(prefix)

            request = {
                'velo_user': cred.service_user_name,
                'velo_pass': cred.password,
                'command': 'get_file',
                'remote_path': remote_file_path,
                'local_path': prefix,
                'filename': filename
            }
            response = velo_request(request)
            if 'Failed to download file' in response:
                print response
                return HttpResponse(status=500)

            path = prefix + filename
            path_components = path.split("/")
            path = os.path.join(
                path_components[path_components.index(cred.service_user_name) + 1:])
            if filename.split('.').pop() == 'png':
                response = {
                    'type': 'image',
                    'location': path
                }
                return HttpResponse(json.dumps(response))
            else:
                out = response.splitlines(True)
                return HttpResponse(out, content_type='text/plain')

        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


def check_velo_initialized(user):
    request = json.dumps({
        'velo_user': user,
        'command': 'is_initialized'
    })
    response = requests.post('http://localhost:8080', request).content
    if 'true' in response:
        return True
    elif 'false' in response:
        return False
    else:
        return 'error'


def velo_request(data):
    if not check_velo_initialized(data['velo_user']):
        request = json.dumps({
            'command': 'init',
            'velo_user': data['velo_user'],
            'velo_pass': data['velo_pass'],
        })
        response = requests.post('http://localhost:8080', request).content
        if 'Success' not in response:
            return 'Failed to initialize velo'
    if 'velo_user' not in data:
        return 'No user in velo request'
    if 'velo_pass' not in data:
        return 'No password in velo request'
    return requests.post('http://localhost:8080', json.dumps(data)).content


@login_required
def new_folder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            foldername = data['foldername']

            cred = Credential.objects.get(
                site_user_name=request.user, service="velo")

            request = {
                'velo_user': cred.service_user_name,
                'velo_pass': cred.password,
                'command': 'create_folder',
                'foldername': foldername
            }

            if velo_request(request) == 'Success':
                return HttpResponse(status=200)
            else:
                return HttpResponse(status=500)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)


@login_required
def save_file(request):
    if request.method == 'POST':
        try:
            incoming_file = json.loads(request.body)
            filename = incoming_file['filename']
            remote_path = incoming_file['remote_path']
            text = incoming_file['text']

            cred = Credential.objects.get(
                site_user_name=request.user, service="velo")

            local_path = os.path.join(
                os.getcwd(), 'userdata', cred.service_user_name)
            remote_path = remote_path[:remote_path.index(filename)]
            print 'filename:', filename, 'remote_path:', remote_path

            try:
                f = open(os.path.join(local_path, filename), 'w')
                f.write(text)
                f.close()
            except Exception as e:
                print_debug(e)
                print 'I/O failure when saving file for velo'
                return HttpResponse(status=500)

            data = {
                'velo_user': cred.service_user_name,
                'velo_pass': cred.password,
                'remote_path': remote_path,
                'local_path': local_path,
                'filename': filename,
                'command': 'save_file'
            }
            if velo_request(data) >= 0:
                return HttpResponse(status=200)
            else:
                print out, err
                return HttpResponse(status=500)
        except Exception as e:
            print_debug(e)
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=404)
