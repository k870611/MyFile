
class parsingSDRList():
    def __init__(self,tempList):
        print("parsingSDRList.__init__()")
        self.listToBeParsed = tempList
        print("list for parsing SDR:",self.listToBeParsed)
        self.finalDict = dict()

    def Run(self):
        # parsing pattern: SEL_Status       | 0x00              | ok

        totalList = list()
        for item in self.listToBeParsed:
            tempDict = dict()
            tempList = item.split("|")
            index = 0
            nameList = ["name","value","status"]
            nameLen = len(nameList)
            for entry in tempList:
                print("entry index:",index)
                tempDict[nameList[index]] = entry
                index += 1

            totalList.append(tempDict)
        self.finalDict["sdr list"] = totalList

        return self.finalDict
