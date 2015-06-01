import VeloAPI
import os


def get_file(filename, filepath):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()
    path = os.getcwd() + '/userdata/' + request.user
    if not os.path.isdir(path):
        os.makedirs(path)

    if velo.download_file(filepath, filename):
        content = open(path + file_to_get['filename']).read()
        print content
    else:
        return -1
