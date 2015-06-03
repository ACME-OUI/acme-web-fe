import VeloAPI
import os
import sys


def save_file(text, remote_path, site_user, velo_username, password, filename):
    try:
        velo_api = VeloAPI.Velo()
        if not velo_api.isJVMStarted():
            velo_api.start_jvm()
        rs = velo_api.init_velo(velo_username, password)

        local_path = os.getcwd() + 'userdata/acmetest/' + filename
        try:
            f = open(local_path, 'w')
            f.write(text)
            f.close()
        except:
            print 'I/O failure when writing file'
            raise

        if velo_api.upload_file(remote_file_path, local_path):
            return 0
            # c = content.splitlines(True)
            # for line in c:
            #     print line
        else:
            return -1
    except:
        raise


save_file(sys.argv[1], sys.argv[2], sys.argv[3],
          sys.argv[4], sys.argv[5], sys.argv[6])
