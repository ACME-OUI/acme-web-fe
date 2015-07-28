from django.test import TestCase
from django.test.client import Client
import VeloAPI
import os
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
    return requests.post('http://localhost:8080', json.dumps(data)).content


class TestVelo(TestCase):

    def test_create_and_delete_folder(self):
        foldername = 'new_folder_test'
        folderpath = '/User Documents/acmetest/'
        data = {
            'velo_user': 'acmetest',
            'velo_pass': 'acmetest',
            'foldername': folderpath + foldername,
            'command': 'create_folder'
        }
        response = velo_request(data)
        self.assertEqual(response, '0')

        data['command'] = 'get_folder'
        data['folder'] = '/User Documents/acmetest'
        response = velo_request(data)
        self.assertTrue(
            folderpath + foldername in response)

        data['command'] = 'delete'
        data['resource'] = folderpath + foldername
        response = velo_request(data)
        self.assertEqual(response, '0')

        data['command'] = 'get_folder'
        data['folder'] = '/User Documents/acmetest'
        response = velo_request(data)
        self.assertFalse(
            folderpath + foldername in response)

    def test_upload_and_download_file(self):
        path = os.getcwd()
        acme = 'acme-web-fe'
        index = path.find(acme)
        path = os.path.join(path[:index], acme, 'userdata/acmetest')
        upload_file = next(os.walk(path))[2][0]

        data = {
            'command': 'save_file',
            'velo_user': 'acmetest',
            'velo_pass': 'acmetest',
            'remote_path': '/User Documents/acmetest/',
            'local_path': path,
            'filename': upload_file
        }
        response = velo_request(data)
        self.assertEqual(response, '0')

        os.remove(os.path.join(path, upload_file))
        data['command'] = 'get_file'
        data['remote_path'] = '/User Documents/acmetest/' + upload_file
        data['local_path'] = path
        response = velo_request(data)
        self.assertEqual(response, '0')
        self.assertTrue(upload_file in next(os.walk(path))[2])
