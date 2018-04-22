

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
