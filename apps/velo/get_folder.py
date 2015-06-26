import VeloAPI
import sys


def get_folder(folder, username, password):
    velo_api = VeloAPI.Velo()
    if not velo_api.isJVMStarted():
        velo_api.start_jvm()

    rm = velo_api.init_velo(username, password)
    try:
        response = velo_api.get_resources(folder)
        return 0
    except:
        return -1

exit_code = get_folder(
    folder=sys.argv[1], username=sys.argv[2], password=sys.argv[3])

sys.exit(exit_code)
