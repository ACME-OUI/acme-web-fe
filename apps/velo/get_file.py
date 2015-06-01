import VeloAPI
import os
import sys


def get_file(remote_file_path, filename, site_user, velo_username, password):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()
    rs = velo_api.init_velo(velo_username, password)
    local_path = os.getcwd() + '/userdata/' + site_user

    if not os.path.isdir(local_path):
        os.makedirs(local_path)

    path = local_path.split('/')
    prefix = ''
    for i in range(path.index(site_user)):
        prefix += path[i] + '/'

    for i in range(path.index(site_user), len(path) - 1):
        if not os.path.isdir(prefix + path[i]):
            prefix += path[i] + '/'
            os.makedirs(prefix)

    if velo_api.download_file(remote_file_path, local_path):
        content = open(local_path + '/' + filename).read()
        print content
    else:
        return -1


get_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
