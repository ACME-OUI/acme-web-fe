import VeloAPI
import os
import sys


def save_file(text, filename, site_user, velo_username, password):
    try:
        velo_api = VeloAPI.Velo()
        if not velo_api.isJVMStarted():
            velo_api.start_jvm()
        rs = velo_api.init_velo(velo_username, password)

        local_path = os.getcwd() + '/userdata/' + velo_username + '/'
        try:
            f = open(local_path + filename, 'w')
            f.write(text)
            f.close()
        except:
            print 'I/O failure when writing file to django server'
            raise

        if velo_api.upload_file(local_path, filename):
            print 'File saved'
            return 0
        else:
            print 'Error saving file'
            return -1
    except:
        raise


save_file(sys.argv[1], sys.argv[2], sys.argv[3],
          sys.argv[4], sys.argv[5])
