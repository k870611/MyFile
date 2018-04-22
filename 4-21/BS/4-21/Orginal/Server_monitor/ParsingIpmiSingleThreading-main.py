import os, io, time, math, asyncio, subprocess, logging, shutil, shlex, tempfile, json
import serverParser.ParsingIpmiSingleThreading as ParsingIpmiSingleThread

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

class getFileList():
    logDir = "logs"
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

    startTime = time.time()

    theParsing = ParsingIpmiSingleThread.ParsingIpmiSingleThreading(filesListForParsing)
    theParsing.Run()

    endTime = time.time()
    timeElapsed = endTime - startTime
    print("Time used for parsing:",timeElapsed)
