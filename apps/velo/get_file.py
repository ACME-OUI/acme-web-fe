import VeloAPI
import os
import sys


def get_file(filename, user, username, password):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()
    rs = velo_api.init_velo(username, password)
    path = os.getcwd() + '/userdata/' + user
    print 'path to file ', path
    if not os.path.isdir(path):
        os.makedirs(path)

    if velo_api.download_file(filename, path):
        content = open(path + file_to_get['filename']).read()
        print content
    else:
        return -1


for arg in sys.argv:
    print arg

get_file(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
