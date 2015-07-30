from django.test import TestCase
from django.test.client import Client
import VeloAPI
import os
import os.path
import requests
import json


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
        print 'Initializing velo for user', data['velo_user']
        request = json.dumps({
            'command': 'init',
            'velo_user': data['velo_user'],
            'velo_pass': data['velo_pass'],
        })
        response = requests.post('http://localhost:8080', request).content
        if 'Success' not in response:
            return 'Failed to initialize velo'

    retry_count = 5
    for i in range(retry_count):
        response = requests.post(
            'http://localhost:8080', json.dumps(data)).content
        if response == '':
            request = json.dumps({
                'command': 'init',
                'velo_user': data['velo_user'],
                'velo_pass': data['velo_pass'],
            })
            requests.post('http://localhost:8080', request)
        else:
            return response


class TestVelo(TestCase):

    def test_create_and_delete_folder(self):
        foldername = 'new_folder_test'
        folderpath = '/User Documents/acmetest/'
        data = {
            'velo_user': 'acmetest',
            'velo_pass': 'acmetest',
            'foldername': foldername,
            'command': 'create_folder'
        }
        response = velo_request(data)
        self.assertEqual(response, 'Success')

        data['command'] = 'get_folder'
        data['folder'] = '/User Documents/acmetest'
        response = velo_request(data)
        print 'foldername:', foldername
        print 'data:', data
        print 'response', response
        self.assertTrue(foldername in response)

        data['command'] = 'delete'
        data['resource'] = folderpath + foldername
        response = velo_request(data)
        self.assertEqual(response, 'Success')

        data['command'] = 'get_folder'
        data['folder'] = '/User Documents/acmetest'
        response = velo_request(data)
        if len(response) < 50:
            print 'response:', response
        print 'data:', data
        self.assertFalse(
            folderpath + foldername in response)

    def test_download_and_upload_file(self):
        path = os.getcwd()
        acme = 'acme-web-fe'
        index = path.find(acme)
        path = os.path.join(path[:index], acme, 'userdata/acmetest')
        # upload_file = next(os.walk(path))[2][0]
        upload_file = 'testSaveFile.txt'

        if os.path.exists(os.path.join(path, upload_file)):
            os.remove(os.path.join(path, upload_file))

        data = {
            'command': 'get_file',
            'velo_user': 'acmetest',
            'velo_pass': 'acmetest',
            'remote_path': '/User Documents/acmetest/' + upload_file,
            'local_path': path,
            'filename': upload_file
        }
        response = velo_request(data)
        print 'data:', data
        print 'response:', response
        # self.assertTrue('Fail' not in response)
        self.assertTrue(upload_file in next(os.walk(path))[2])

        data = {
            'command': 'save_file',
            'velo_user': 'acmetest',
            'velo_pass': 'acmetest',
            'remote_path': '/User Documents/acmetest/',
            'local_path': path,
            'filename': upload_file
        }
        print 'sending request with data', data
        response = velo_request(data)
        self.assertTrue('Failed' not in response)
