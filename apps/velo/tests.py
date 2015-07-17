from django.test import TestCase
from django.test.client import Client
import VeloAPI
import os


def setup():
    global v, r
    v = VeloAPI.Velo()
    v.start_jvm()
    r = v.init_velo('acmetest', 'acmetest')


class TestVelo(TestCase):

    def test_create_and_delete_folder(self):
        foldername = 'new_folder_test'
        folderpath = '/User Documents/acmetest/'
        self.assertEqual(v.create_folder(foldername), 0)
        self.assertTrue(
            folderpath + foldername in v.get_homefolder_resources())
        self.assertEqual(v.delete_resource(folderpath + foldername), 0)
        self.assertFalse(
            folderpath + foldername in v.get_homefolder_resources())

    def test_upload_and_download_file(self):
        path = os.getcwd()
        acme = 'acme-web-fe'
        index = path.find(acme)
        path = path[:index] + acme + '/userdata/acmetest'
        upload_file = next(os.walk(path))[2][3]
        ret = v.upload_file('/User Documents/acmetest/', path, upload_file)
        self.assertEqual(ret, 0)

        os.remove(path + '/' + upload_file)

        ret = v.download_file('/User Documents/acmetest/' + upload_file, path)
        self.assertEqual(ret, 0)
        self.assertTrue(upload_file in next(os.walk(path))[2])
