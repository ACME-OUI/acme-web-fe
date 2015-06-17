import VeloAPI
import sys


def get_folder(folder, username, password):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()

    rm = velo_api.init_velo(username, password)
    response = velo_api.get_resources(folder)

    return response

get_folder(sys.argv[1], sys.argv[2], sys.argv[3])
