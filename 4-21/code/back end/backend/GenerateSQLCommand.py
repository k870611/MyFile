import os, io, time, math, asyncio, subprocess, logging, shutil, shlex, tempfile, json

#
# id         server      port   user   password   extraopt    sessions
# ===  ================= ===== ====== ========== =========== ==========
#  1    192.168.100.100   623   root     root    -I lanplus      2
#  2    192.168.100.101   623   root     root    -I lanplus      3
# 
#   id for server         task    freq   id as offset (omitted)   next run
# ==================== ========= ====== ======================== ===============
#  1 (192.168.100.100)  sdrlist     5            1                1523500000000
#
# if (currenttime - offset) % freq == 0, perform task

class generateSQLCommands():

    triggerPeriod = 500
    logDir = "logs"
    newDir = "output"
    delimiter = ""

    def __init__(self,targetFile):
        print("ParsingIpmi,__init__()")
        print("file to be parsed:",targetFile)
        # init all local variables
        self.plansDict = dict()
        self.planList = list()
        self.resultsDict = dict()
    # flags for diciding we are handling plans or results
        self.parsingPlans = True

        self.fileToBeParsed = targetFile
        currenttime = self._get_current_time()
        self.expireTime = currenttime
        # self.lastRun = currenttime

    def _get_current_time(self):
        return math.floor(time.time() * 1000 / self.triggerPeriod) * self.triggerPeriod

    def run(self):
        print("Run()")

        # get target file for parsing
       # with open(self.fileToBeParsed, "r") as f:
        with open(self.fileToBeParsed) as json_data:
            jsonData = json.load(json_data)
            print(jsonData)

            print("sel list:",jsonData["sel list"])
            for key in jsonData.keys():
                print(key)

class getFileList():
    logDir = "output"
    fileList = list()

    def __init__(self):
        print("getFileList init")

    def Run(self):
        currDir = os.getcwd()
        print("currentdir:",currDir)
        newDir = os.path.join(os.getcwd(),self.logDir)
        print("new dir:",newDir)
        tempFileLists = os.listdir(newDir)
        #print("target files:",tempFileLists)
        
        for file in tempFileLists:
            targetFile = os.path.join(newDir,file)
            #print("target file:",targetFile)
            self.fileList.append(targetFile)

        #print("\n\n\n final files to be parsed:",self.fileList)
        return self.fileList

if __name__ == '__main__':
    filesListForParsing = list()
    getFile = getFileList()
    filesListForParsing = getFile.Run()

    #print("file numbers:",len(filesListForParsing))
    
    numOfParsed = 1
    startTime = time.time()
    for file in filesListForParsing:
        print("\n\n\n")
        print("######################################################")
        print(" New parsing loop for:",file)

        sqlConvert = generateSQLCommands(file)
        sqlConvert.run()

    endTime = time.time()
    timeElapsed = endTime - startTime
    print("Time used for parsing:",timeElapsed)

    '''

    target = "/home/stanley/workspace/Server_monitor/logs/output-2-20180413170208.txt.2"
    theParsing = ParsingIpmi(target)
    theParsing.Run()
    '''    
