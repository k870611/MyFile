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
