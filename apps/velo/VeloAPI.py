import jpype
import time
from jpype import *
import os

jvmPath = jpype.getDefaultJVMPath()


def start_jvm():
    # include the velo python API jar file here
    path = os.getcwd()
    acme = 'acme-web-fe'
    index = path.find(acme)
    path = path[:index]

    if jpype.isJVMStarted():
        return
    jpype.startJVM(
        jvmPath, "-Djava.class.path=" + path + "acme-web-fe/static/java/VeloAPI.jar")

    global velo, cms, jobConfig, fileObj, tifConstants

    velo = JPackage("velo").mgr.VeloManager
    cms = JPackage("gov").pnnl.velo.model.CmsPath
    jobConfig = JPackage("gov").pnnl.velo.tif.model.JobConfig
    tifConstants = JPackage("gov").pnnl.velo.util.VeloTifConstants


class Velo(object):

    def __init__(self):
        self.fileServerMap = None
        self.filesToDownload = None
        self.resMgr = None

    def isJVMStarted(self):
        return jpype.isJVMStarted()

    def init_velo(self, username, password):
        self.fileServerMap = jpype.java.util.HashMap()
        self.filesToDownload = jpype.java.util.ArrayList()
        self.resMgr = velo.init(username, password)
        return self.resMgr

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
        try:
            homeFolder = Velo.get_homefolder(self)
            cmspath = cms(homeFolder).append(foldername)
            self.resMgr.createFolder(cmspath)
            return 0
        except:
            return -1

    # upload file in velo
    def upload_file(self, remote_path, local_path, filename):
        try:
            fileObj = jpype.java.io.File(local_path + "/" + filename)
            cmsfilepath = cms(remote_path).append(filename)
            self.fileServerMap.put(fileObj, cmsfilepath)
            self.resMgr.bulkUpload(self.fileServerMap, None)
            return 0
        except:
            return -1

    # download file from velo
    def download_userhome_file(self, filename, location):
        destFolder = jpype.java.io.File(location)
        homeFolder = Velo.get_homefolder(self)
        cmspath = homeFolder.append(filename)
        self.filesToDownload.add(cmspath)
        self.resMgr.bulkDownload(self.filesToDownload, destFolder)

    def download_file(self, filepath, location):  # download file from velo
        try:
            destFolder = jpype.java.io.File(location)
            cmsfilepath = cms(filepath)
            self.filesToDownload.add(cmsfilepath)
            self.resMgr.bulkDownload(self.filesToDownload, destFolder)
            return 0
        except:
            return -1

    # download multiple files from velo
    def download_files(self, filepaths, location):
        destFolder = jpype.java.io.File(location)
        for filepath in filepaths:
            cmsfilepath = cms(filepath)
            self.filesToDownload.add(cmsfilepath)
        self.resMgr.bulkDownload(self.filesToDownload, destFolder)
        print "Files downloaded"

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
        self.filesToDownload.add(joberrfile)
        self.filesToDownload.add(joboutfile)
        self.filesToDownload.add(joboutput)
        self.resMgr.bulkDownload(self.filesToDownload, destFolder)

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
        self.resMgr.createFolder(contextPath)
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
            ress = self.resMgr.getChildren(cmsparentPath)
            for i in range(len(ress)):
                print ress[i]
                ret.append(ress[i].toString() + ',')
                if isinstance(ress[i], Folder):
                    sub = Velo.get_resources(self, ress[i].toString())
                    for r in sub:
                        ret.append(r + ',')
        except:
            print 'resource ', parentPath, 'does not exist'

        return ret

    # returns all the subfolders in users' home folder
    def get_homefolder_resources(self):
        folder = self.resMgr.getHomeFolder()
        ress = self.resMgr.getChildren(folder.getPath())
        ret = []
        for i in range(len(ress)):
            ret.append(ress[i].toString())
        return ret

    def delete_resource(self, resourcePath):  # delete single resource
        try:
            cmsfilepath = cms(resourcePath)
            self.resMgr.deleteResource(cmsfilepath)
            return 0
        except:
            return -1

    def delete_resources(self, resources):  # delete multiple resources
        resourceToDelete = jpype.java.util.ArrayList()
        for res in resources:
            cmsfilepath = cms(res)
            resourceToDelete.add(cmsfilepath)
        self.resMgr.deleteResources(resourceToDelete)

    def get_homefolder(self):  # get user's home folder
        folder = self.resMgr.getHomeFolder()
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
