import VeloAPI
import os
import sys


def delete(name, velo_username, password):

    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()
    rs = velo_api.init_velo(velo_username, password)

    try:
        velo_api.delete_resource(name)
        return 0
    except:
        return -1


exit_code = delete(
    name=sys.argv[1], velo_username=sys.argv[2], password=sys.argv[3])

sys.exit(exit_code)
