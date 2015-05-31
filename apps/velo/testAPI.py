'''
Created on Mar 16, 2015

@author: raju332
'''
import VeloAPI

velo_api = VeloAPI.Velo()
velo_api.start_jvm()  # start jvm
# provide velo username and password
print 'starting velo initialization'
velo_api.init_velo("acmetest", "acmetest")
print 'retrieving home folder resources'
velo_api.get_homefolder_resources()  # get directory from user home folder
print " "
# get resources from the specified path
filepath = "/User Documents/acmetest/fake_acme_case_2015-04-28_07-45-44"
print 'retrieving resource at', filepath
velo_api.get_resources(filepath)
print 'creating test folder'
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
