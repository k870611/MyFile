import os, io, time, math, asyncio, subprocess, logging, shutil, shlex, tempfile, json
import parser.generateSQLCommand as generateSQLCommand
import parser.getFileList as getFileList

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


if __name__ == '__main__':
    filesListForParsing = list()
    getFile = getFileList.getFileList()
    filesListForParsing = getFile.Run()

    #print("file numbers:",len(filesListForParsing))
    
    numOfParsed = 1
    startTime = time.time()
    for eachFile in filesListForParsing:
        print("\n\n\n")
        print("######################################################")
        print(" New parsing loop for:",eachFile)

        sqlConvert = generateSQLCommand.generateSQLCommand(eachFile)
        sqlConvert.run()

    endTime = time.time()
    timeElapsed = endTime - startTime
    print("Time used for parsing:",timeElapsed)

    '''

    target = "/home/stanley/workspace/Server_monitor/logs/output-2-20180413170208.txt.2"
    theParsing = ParsingIpmi(target)
    theParsing.Run()
    '''    
