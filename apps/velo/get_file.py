import VeloAPI
import os


def get_file(filename, user, username, password):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()
    rs = velo_api.init_velo(username, password)
    path = os.getcwd() + '/userdata/' + user
    if not os.path.isdir(path):
        os.makedirs(path)

    if velo_api.download_file(filepath, filename):
        content = open(path + file_to_get['filename']).read()
        print content
    else:
        return -1
