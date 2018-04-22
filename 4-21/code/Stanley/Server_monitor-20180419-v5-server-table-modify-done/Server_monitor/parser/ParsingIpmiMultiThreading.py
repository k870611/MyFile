import os, io, time, math, asyncio, subprocess, logging, shutil, shlex, tempfile, json
import threading
import parser.ipmiParser.parsingSDRList as parsingSDRList
import parser.ipmiParser.parsingSELList as parsingSELList
import parser.mysqlDBDeployment as mysqlDBDeployment

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

class ParsingIpmiMultiThreading(threading.Thread):

    triggerPeriod = 500
    logDir = "logs"
    newDir = "result"
#    fileToBeParsed = "output-2-20180413165508.txt.2"
#    fileToBeParsed = "output-1-20180413165204.txt.2"
#    plansDict = dict()
#    planList = list()
    delimiter = ""
#    resultsDict = dict()
    # flags for diciding we are handling plans or results
#    parsingPlans = True

    def __init__(self,totalThreads,threadID, name,targetFileList):
        print("ParsingIpmi,__init__()")
        super(ParsingIpmiMultiThreading, self).__init__()
#        print("file to be parsed:",targetFileList)
        # init all local variables
        self.plansDict = dict()
        self.planList = list()
        self.resultsDict = dict()
    # flags for diciding we are handling plans or results
        self.parsingPlans = True

        self.fileListToBeParsed = list()
        currenttime = self._get_current_time()
        self.expireTime = currenttime
        self.totalThreads = totalThreads
        self.threadID = threadID
        # self.lastRun = currenttime

        for item in targetFileList:
            print("old file name:",item)
            print("tail:",item[-1])
            if item[-1] == "2":
                self.fileListToBeParsed.append(item)

        print("===>final files:",self.fileListToBeParsed)

    def _get_current_time(self):
        return math.floor(time.time() * 1000 / self.triggerPeriod) * self.triggerPeriod

    def run(self):
        print("Run()")

        fileList = list()
        index = 0
        for item in self.fileListToBeParsed:
            index += 1
            if index % self.totalThreads == self.threadID:
                print("thread id:",self.threadID)
                fileList.append(item)
            if self.totalThreads == self.threadID:
                if index % self.totalThreads == 0:
                    fileList.append(item)

        print("file to be parsed:",fileList)

        for targetFile in fileList:
            newTempFile = targetFile + ".tmp"
            os.rename(targetFile, newTempFile)
            # get target file for parsing
            with open(newTempFile, "r") as f:
                for line in f.readlines():
                #    print("line:",line)
                    if "Time=" in line:
                        print("Delimiter:",line)
                        self.parsingPlans = False

                    if self.parsingPlans is True:
                        #print("we are parsing plans")
                        if "#" not in line:
                            if "raw" not in line:
                                print("target command:",line)
                                self.planList.append(line.strip("\n"))

                print("command plans in 1st phase:",self.planList)
      
                itemIndex = 1
        
                for item in self.planList:
            
                    print("\n\n\n===>start to insert results for command:",item)
                    # rewind to parse th result
                    f.seek(0)
                    self.parsingPlans = True
                    # pivotCount is used to count "01 84 14 03 00 00 00 00"
                    pivotCount = 0
                    tempList = list()        

                    for line in f.readlines():
                        print("line:",line)
                        pivot = False

                        if "Time=" in line:
                            print("Delimiter:",line)
                            self.parsingPlans = False

                        if self.parsingPlans is False:
                            print("we are parsing results")
                            if "Error:" in line:
                                tempList.append(line.strip("\n"))
                                break
                            if "# Time=" in line:
                                continue
                            elif "01 84 14 03 00"  in line:
                                pivot = True
                                pivotCount += 1
                                continue
                            else:
                                if pivotCount == itemIndex:
                                    print("results to be inserted:",line)
                                    print("pivotCount:",pivotCount,"itemIndex:",itemIndex)
                                    tempList.append(line.strip("\n"))
                                else:
                                    print("=>results to be skipped:",line) 
                                    print("pivotCount:%d,itemIndex:%d",pivotCount,itemIndex)

                    # use parsing functions for different handling
                    print("key:",item)
                    if item == "sdr list":
                        parsingSdr = parsingSDRList.parsingSDRList(tempList)
                        tempDict = parsingSdr.Run()
                        self.resultsDict["sdr list"] = tempDict["sdr list"]
                    elif item == "sel list":
                        parsingSel = parsingSELList.parsingSELList(tempList)
                        tempDict = parsingSel.Run()
                        self.resultsDict["sel list"] = tempDict["sel list"]
                    else:
                        self.resultsDict[item] = tempList

                    itemIndex += 1

            # remove original file
            os.remove(newTempFile)


        #print("command plans in 2nd phase:",self.planList)
        print("number of dict:",len(self.resultsDict))

        print("\n\n\n\n=============================")

#        for item in self.planList:
#            print("dict key name:",item)
#            print("dump item:",self.resultsDict[item])

        '''
        for item in fileList:
            print("old file name:",item)
            newFile = item[0:-1] + "3"
            print("new file name:",newFile)

            with open(newFile,"w") as f:
                f.write(json.dumps(self.resultsDict))
        '''

        DBCreate = mysqlDBDeployment.mysqlDBDeployment()

        DBName = "server_management"

        # build table - server_sdr
        TableName = "server_sdr"

        for item in fileList:
            print("old file name:",item)
            newFile = item[0:-1] + "4"
            print("new file name:",newFile)

            with open(newFile,"w") as f:
                newJson = dict()
                newJson["sdr list"] = self.resultsDict["sdr list"]


                newString = str(newJson["sdr list"])

                finalString = DBCreate.replaceDataQuotation(newString)

                print("\n\n ## string:",finalString)

                finalCommand = DBCreate.encapsulationCommand(finalString)


                fieldValueForStoreProcedure = finalCommand
                #DBCreate.storeProcedureInsertServerSdr(DBName,TableName,fieldValueForStoreProcedure)


                #f.write(json.dumps(self.resultsDict))        
        

                newCommand = DBCreate.generateCommandInsertServerSdr(fieldValueForStoreProcedure)
               #command = "DBCreate.storeProcedureInsertServerSdr("  + fieldValueForStoreProcedure + ")"
                print("\n\n\n==> command for write:",newCommand)
                f.write(newCommand)


