'''
Created on Mar 16, 2015

@author: raju332
'''
import VeloAPI

velo_api = VeloAPI.Velo()
velo_api.start_jvm() #start jvm
#provide velo username and password
velo_api.init_velo("<username>", "<password>")
velo_api.create_folder("testFolder") #provide folder name
velo_api.upload_file("C:/Python34/nf", "file.txt") #specify location of file and name of file
velo_api.create_instance() # creates a tool instance for ACME fake job
velo_api.create_remotelink()
jobconfig = velo_api.launch_job("<acmetest username>") # launch the fake job, provide username for the acmetest server
velo_api.get_job_status()
velo_api.shutdown_jvm() #shutdown jvm