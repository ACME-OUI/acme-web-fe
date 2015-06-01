import VeloAPI
import os
import sys


def get_file(remote_file_path, filename, site_user, velo_username, password):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()
    rs = velo_api.init_velo(velo_username, password)
    local_path = os.getcwd() + '/userdata/' + site_user

    path = local_path.split('/')
    remote_path = remote_file_path.split('/')
    user_folder_index = remote_path.index(velo_username)
    prefix = ''
    for i in range(path.index(site_user)):
        prefix += path[i] + '/'

    for i in range(user_folder_index, len(remote_path) - 1):
        if not os.path.isdir(prefix + remote_path[i]):
            prefix += remote_path[i] + '/'
            print 'making new dir ', prefix
            os.makedirs(prefix)

    if velo_api.download_file(remote_file_path, local_path):
        content = open(local_path + '/' + filename).read()
        print content
    else:
        return -1


get_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
