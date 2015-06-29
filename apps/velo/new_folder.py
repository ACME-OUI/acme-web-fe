import VeloAPI
import sys


def new_folder(foldername, velo_username, password):
    try:
        velo_api = VeloAPI.Velo()
        if not velo_api.isJVMStarted():
            velo_api.start_jvm()
        rs = velo_api.init_velo(velo_username, password)

        if velo_api.create_folder(foldername) >= 0:
            print "Created new folder"
            return 0
        else:
            print 'Failed to create new folder'
            return -1
    except:
        raise


exit_code = new_folder(
    foldername=sys.argv[1], velo_username=sys.argv[2], password=sys.argv[3])

sys.exit(exit_code)
