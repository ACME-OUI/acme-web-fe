'''
Created on Mar 16, 2015

@author: raju332
'''
import VeloAPI

velo_api = VeloAPI.Velo()
velo_api.start_jvm()  # start jvm
# provide velo username and password
velo_api.init_velo("<username>", "<password>")
velo_api.get_homefolder_resources()  # get directory from user home folder
print " "
# get resources from the specified path
velo_api.get_resources(
    "/User Documents/admin/fake_acme_case_04-03-2015_16-11-27")
velo_api.create_folder("testFolder")  # provide folder name
# specify location of file and name of file
velo_api.upload_file("C:/Python34/nf", "file.txt")
# specify name of the file in Velo to download and the local directory
# location to save the file
velo_api.download_file("/User Documents/admin/file.txt",
                       "C:/Users/raju332/Documents/VeloPythonAPI/test")
velo_api.create_instance()  # creates a tool instance for ACME fake job
velo_api.create_remotelink()
# launch the fake job, provide username for the acmetest server and the
# location to download the output files
jobconfig = velo_api.launch_job(
    "bibiraju", "C:/Users/raju332/Documents/VeloPythonAPI/test")
velo_api.get_job_status()
velo_api.shutdown_jvm()  # shutdown jvm
