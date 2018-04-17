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

class ParsingIpmi():

    triggerPeriod = 500
    logDir = "logs"
#    fileToBeParsed = "output-2-20180413165508.txt.2"
#    fileToBeParsed = "output-1-20180413165204.txt.2"
#    plansDict = dict()
#    planList = list()
    delimiter = ""
#    resultsDict = dict()
    # flags for diciding we are handling plans or results
#    parsingPlans = True

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

    def Run(self):
        print("Run()")

        # get target file for parsing
        with open(self.fileToBeParsed, "r") as f:
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
                    parsingSdr = parsingSDRList(tempList)
                    tempDict = parsingSdr.Run()
                    self.resultsDict["sdr list"] = tempDict["sdr list"]
                elif item == "sel list":
                    parsingSel = parsingSELList(tempList)
                    tempDict = parsingSel.Run()
                    self.resultsDict["sel list"] = tempDict["sel list"]
                else:
                    self.resultsDict[item] = tempList
                itemIndex += 1


        #print("command plans in 2nd phase:",self.planList)
        print("number of dict:",len(self.resultsDict))

        print("\n\n\n\n=============================")

        for item in self.planList:
            print("dict key name:",item)
            print("dump item:",self.resultsDict[item])


        print("old file name:",self.fileToBeParsed)
        newFile = self.fileToBeParsed[0:-1] + "3"
        print("new file name:",newFile)

        with open(newFile,"w") as f:
            f.write(json.dumps(self.resultsDict))
        
class parsingSDRList():
    def __init__(self,tempList):
        print("parsingSDRList.__init__()") 
        self.listToBeParsed = tempList
        self.finalDict = dict()

    def Run(self):
        # parsing pattern: SEL_Status       | 0x00              | ok

        totalList = list()
        for item in self.listToBeParsed:
            tempDict = dict()
            tempList = item.split("|")
            index = 0
            nameList = ["name","value","status"]
            for entry in tempList:
                tempDict[nameList[index]] = entry
                index += 1

            totalList.append(tempDict)
        self.finalDict["sdr list"] = totalList
        
        return self.finalDict 
       

class parsingSELList():
    def __init__(self,tempList):
        print("parsingSELList.__init__()")
        self.listToBeParsed = tempList
        self.finalDict = dict()

    def Run(self):
        # parsing pattern 1: 80 | 01/01/2000 | 00:01:14 | Fan #0x75 | Lower Critical going low
        # parsing pattern 2: aa | 01/01/2000 | 00:00:53 | Power Supply #0xa9 | Presence detected | Asserted

        totalList = list()
        for item in self.listToBeParsed:
            tempDict = dict()
            tempList = item.split("|")
            if len(tempList) == 5:
            
                index = 0
                nameList = ["sel_id","date","hour","sel_name","condition"]
                for entry in tempList:
                    print("item:",entry)
                    tempDict[nameList[index]] = entry
                    index += 1

                totalList.append(tempDict)
            else:

                index = 0
                nameList = ["sel_id","date","hour","sel_name","condition","assert_tag"]
                for entry in tempList:
                    print("item:",entry)
                    tempDict[nameList[index]] = entry
                    index += 1

                totalList.append(tempDict)

        self.finalDict["sel list"] = totalList

        return self.finalDict 


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

    #print("file numbers:",len(filesListForParsing))
    
    numOfParsed = 1
    startTime = time.time()
    for file in filesListForParsing:
        print("\n\n\n")
        print("######################################################")
        print(" New parsing loop for:",file)

        theParsing = ParsingIpmi(file)
        theParsing.Run()
        numOfParsed += 1
        if numOfParsed == 3:
            break

    endTime = time.time()
    timeElapsed = endTime - startTime
    print("Time used for parsing:",timeElapsed)
    '''

    target = "/home/stanley/workspace/Server_monitor/logs/output-2-20180413170208.txt.2"
    theParsing = ParsingIpmi(target)
    theParsing.Run()
    '''    
