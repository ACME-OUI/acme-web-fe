'''
Created on Mar 16, 2015

@author: raju332
'''
import jpype
import time
from jpype import *
jvmPath = jpype.getDefaultJVMPath()


class Velo:

    def __init__(self):
        pass

    def start_jvm(self):
        # include the velo python API jar file here
        jpype.startJVM(
            jvmPath, "-Djava.class.path=/home/baldwin/acme-web-fe/static/java/VeloAPI.jar")
        global velo, cms, jobConfig, fileObj, tifConstants, fileServerMap, filesToDownload
        velo = JPackage("velo").mgr.VeloManager
        cms = JPackage("gov").pnnl.velo.model.CmsPath
        jobConfig = JPackage("gov").pnnl.velo.tif.model.JobConfig
        tifConstants = JPackage("gov").pnnl.velo.util.VeloTifConstants

        fileServerMap = jpype.java.util.HashMap()
        filesToDownload = jpype.java.util.ArrayList()

    def init_velo(self, username, password):
        global resMgr
        resMgr = velo.init(username, password)
        return resMgr

    def get_cms_service(self):
        cms = velo.getCmsService()
        return cms

    def get_job_status(self):
        cms_service = Velo.get_cms_service(self)

        status = cms_service.getProperty(
            con.getContextPath(), tifConstants.JOB_STATUS)
        starttime = cms_service.getProperty(
            con.getContextPath(), tifConstants.JOB_START_TIME)
        stoptime = cms_service.getProperty(
            con.getContextPath(), tifConstants.JOB_STOP_TIME)
        submittime = cms_service.getProperty(
            con.getContextPath(), tifConstants.JOB_SUBMIT_TIME)
        # print "Job Status:", status

    def create_folder(self, foldername):  # create a folder
        homeFolder = Velo.get_homefolder(self)
        cmspath = cms(homeFolder).append(foldername)
        resMgr.createFolder(cmspath)

    def upload_file(self, location, filename):  # upload file in velo
        fileObj = jpype.java.io.File(location + "/" + filename)
        homeFolder = Velo.get_homefolder(self)
        cmspath = homeFolder.append(filename)
        fileServerMap.put(fileObj, cmspath)
        # velo.uploadFile(location, filename , fileServerMap, None)
        resMgr.bulkUpload(fileServerMap, None)

    # download file from velo
    def download_userhome_file(self, filename, location):
        destFolder = jpype.java.io.File(location)
        homeFolder = Velo.get_homefolder(self)
        cmspath = homeFolder.append(filename)
        filesToDownload.add(cmspath)
        resMgr.bulkDownload(filesToDownload, destFolder)

    def download_file(self, filepath, location):  # download file from velo
        destFolder = jpype.java.io.File(location)
        cmsfilepath = cms(filepath)
        filesToDownload.add(cmsfilepath)
        resMgr.bulkDownload(filesToDownload, destFolder)
        print "File downloaded"

    # download the job outputs
    def download_job_outputs(self, contextPathName, location):
        destFolder = jpype.java.io.File(location)
        homeFolder = Velo.get_homefolder(self)
        joberrfile = homeFolder.append(contextPathName).append(
            "Outputs").append("job.err")
        joboutfile = homeFolder.append(contextPathName).append(
            "Outputs").append("job.out")
        joboutput = homeFolder.append(contextPathName).append(
            "Outputs").append("output.txt")
        filesToDownload.add(joberrfile)
        filesToDownload.add(joboutfile)
        filesToDownload.add(joboutput)
        resMgr.bulkDownload(filesToDownload, destFolder)

    def launch_job(self, acmeusername, location):  # launch the fake job
        secMgr = Velo.get_security_manager(self)
        config = jobConfig("fake_acme_job")
        config.setCmsUser(secMgr.getUsername())
        config.setCodeId("acmeworkflow")
        codereg = JPackage("gov").pnnl.velo.tif.service.CodeRegistry
        config.setCodeVersion(codereg.VERSION_DEFAULT)
        # specify the fake_case directory
        remoteDir = "/data/acme/velotestruns/fake_acme_case"
        config.setRemoteDir(remoteDir)

        remotedirfile = jpype.java.io.File(remoteDir).getName()

        now = time.strftime("%Y-%m-%d_%H-%M-%S")
        contextPathName = remotedirfile + "_" + now
        contextPath = Velo.get_homefolder(self).append(contextPathName)
        resMgr.createFolder(contextPath)
        time.sleep(5)
        print "folder created: ", contextPathName
        config.setContextPath(contextPath.toAssociationNamePath())
        config.setDoNotQueue(True)
        config.setJobId(contextPathName)
        config.setMachineId("localhost")
        # provide username for the acmetest server as the fake job is in
        # acmetest
        config.setUserName(acmeusername)
        config.setPollingInterval(5)
        config.setLocalMonitoring(jpype.java.lang.Boolean(False))
        jobLaunchService = Velo.get_job_launch_service(self)
        global job_config
        job_config = jobLaunchService.launchJob(config, None)
        global con
        con = config
        # job_config = velo.launchJob()
        print "Fake Job submitted"
        print "Waiting for job output files"
        time.sleep(60)
        print "Job output files downloaded to ", location
        Velo.download_job_outputs(self, contextPathName, location)
        return job_config

    def get_resources(self, parentPath):
        Folder = JPackage("gov").pnnl.cat.core.resources.IFolder
        cmsparentPath = cms(parentPath)
        ret = []
        try:
            ress = resMgr.getChildren(cmsparentPath)
        except:
            print 'resource ', parentPath, 'does not exist'
        for i in range(len(ress)):
            print ress[i]
            ret.append(ress[i])
            if isinstance(ress[i], Folder):
                Velo.get_resources(self, ress[i].toString())

    # returns all the subfolders in users' home folder
    def get_homefolder_resources(self):
        folder = resMgr.getHomeFolder()
        ress = resMgr.getChildren(folder.getPath())
        ret = []
        for i in range(len(ress)):
            ret.append(ress[i].toString())
        return ret
        # Velo.get_resources(self,folder.toString())

    def get_homefolder(self):  # get user's home folder
        folder = resMgr.getHomeFolder()
        home_folder = folder.getPath()
        return home_folder

    def create_instance(self):  # create tool instance in user's home folder
        velo.createToolInstance()

    def create_remotelink(self):
        velo.remoteLink()

    def get_job_launch_service(self):
        jobService = velo.getJobLaunchService()
        return jobService

    def get_security_manager(self):
        secmgr = velo.getSecurityManager()
        return secmgr

    def shutdown_jvm(self):
        jpype.shutdownJVM()
