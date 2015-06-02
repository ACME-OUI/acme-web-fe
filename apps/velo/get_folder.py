import VeloAPI
import sys


def get_folder(folder):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()

    rm = velo_api.init_velo('acmetest', 'acmetest')
    response = velo_api.get_resources(folder)

    return response

get_folder(sys.argv[1])
