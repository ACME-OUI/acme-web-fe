import VeloAPI
import os
import sys


def get_file(remote_file_path, local_path, filename, site_user, velo_username, password):
    try:
        velo_api = VeloAPI.Velo()
        if not velo_api.isJVMStarted():
            velo_api.start_jvm()
        rs = velo_api.init_velo(velo_username, password)

        if velo_api.download_file(remote_file_path, local_path) >= 0:
            content = open(local_path + filename).read()
            print content
            return 0
        else:
            print 'NO SUCH FILE', remote_file_path, local_path
            return -1
    except:
        raise


exit_code = get_file(remote_file_path=sys.argv[1], local_path=sys.argv[2], filename=sys.argv[3],
                     site_user=sys.argv[4], velo_username=sys.argv[5], password=sys.argv[6])

sys.exit(exit_code)
