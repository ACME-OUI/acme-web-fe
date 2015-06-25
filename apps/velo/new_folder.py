import VeloAPI
import sys


def new_folder(foldername, velo_username, password):
    try:
        velo_api = VeloAPI.Velo()
        if not velo_api.isJVMStarted():
            velo_api.start_jvm()
        rs = velo_api.init_velo(velo_username, password)

        if velo_api.create_folder(foldername) >= 0:
            print "Creaded new folder"
            return 0
        else:
            print 'Failed to create new folder'
    except:
        raise


new_folder(sys.argv[1], sys.argv[2], sys.argv[3])
