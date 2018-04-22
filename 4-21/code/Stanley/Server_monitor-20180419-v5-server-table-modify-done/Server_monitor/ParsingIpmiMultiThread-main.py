import os, io, time, math, asyncio, subprocess, logging, shutil, shlex, tempfile, json
import threading
import parser.ParsingIpmiMultiThreading as ParsingIpmi
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
    threadNum = 4
    filesListForParsing = list()
    getFile = getFileList()
    filesListForParsing = getFile.Run()

    #print("file numbers:",len(filesListForParsing))
    
    startTime = time.time()

    '''
    old method for single threading
    for file in filesListForParsing:
        print("\n\n\n")
        print("######################################################")
        print(" New parsing loop for:",file)

        theParsing = ParsingIpmi(file)
        theParsing.Run()
    '''
    thread1 = ParsingIpmi.ParsingIpmiMultiThreading(4,1, "Thread-1", filesListForParsing)
    thread2 = ParsingIpmi.ParsingIpmiMultiThreading(4,2, "Thread-2", filesListForParsing)
    thread3 = ParsingIpmi.ParsingIpmiMultiThreading(4,3, "Thread-3", filesListForParsing)
    thread4 = ParsingIpmi.ParsingIpmiMultiThreading(4,4, "Thread-4", filesListForParsing)

    # Start new Threads
    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    # Add threads to thread list
    threads.append(thread1)
    threads.append(thread2)
    threads.append(thread3)
    threads.append(thread4)

    # Wait for all threads to complete
    for t in threads:
        t.join()
    print("Exiting Main Thread")



    endTime = time.time()
    timeElapsed = endTime - startTime
    print("Time used for parsing:",timeElapsed)


