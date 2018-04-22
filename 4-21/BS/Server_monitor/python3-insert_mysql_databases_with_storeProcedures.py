import time, os, json
import parser.mysqlDBDeployment as mysqlDBDeployment


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
    DBCreate = mysqlDBDeployment.mysqlDBDeployment()

    DBName = "server_management"

    # build table - server_sdr
    TableName = "server_sdr"

    print("insert 1st basic data into  - server_sdr")
    fieldName = "(id,server_sdr_id,server_sdr_name,server_sdr_status,server_sdr_value,server_id)"
    fieldValue = "(NULL, '1','CPU0_Temp','ok','48.000','1')"
    #DBCreate.insertData(DBName,TableName,fieldName,fieldValue)


    # insert data with json format
    print("insert 1st basic data into  - server_sdr")
    fieldName = "(id,server_sdr_id,server_sdr_name,server_sdr_status,server_sdr_value,server_id,json_value)"
    fieldValue = '''(NULL, '1','CPU0_Temp','ok','48.000','2','{"sdr list": [{"value": " 0x00              ", "status": " ok", "name": "SEL_Status       "}, {"value": " 0x00              ", "status": " ok", "name": "IPMI_Watchdog    "}]}')'''

    fieldValueForStoreProcedure = '''NULL; '1';'CPU0_Temp';'ok';'48.000';'2';'{"sdr list": [{"value": " 0x00              ", "status": " ok", "name": "SEL_Status       "}, {"value": " 0x00              ", "status": " ok", "name": "IPMI_Watchdog    "}]}' '''
    DBCreate.storeProcedureInsertServerSdr(DBName,TableName,fieldValueForStoreProcedure)

    getFile = getFileList()
    filesListForParsing = getFile.Run()
    fileListToBeParsed = list()
    print("file lise:",filesListForParsing)

    for item in filesListForParsing:
        print("old file name:",item)
        print("tail:",item[-1])
        if item[-1] == "3":
            fileListToBeParsed.append(item)



    for eachFile in fileListToBeParsed:
        with open(eachFile) as json_data:
            jsonData = json.load(json_data)
        #    print(jsonData)

            print("sdr list:",jsonData["sdr list"])
    #        for key in jsonData.keys():
    #            print(key)
        newJson = dict()
        newJson["sdr list"] = jsonData["sdr list"]
    #    print("new json:",newJson["sdr list"])

        #newSdrInfo = '''NULL; '1';'CPU0_Temp';'ok';'48.000';'2';'{"sdr list":'''
        newString = str(newJson["sdr list"])

        finalString = DBCreate.replaceDataQuotation(newString)

        print("\n\n ## string:",finalString)

        finalCommand = DBCreate.encapsulationCommand(finalString)


        fieldValueForStoreProcedure = finalCommand
        DBCreate.storeProcedureInsertServerSdr(DBName,TableName,fieldValueForStoreProcedure)

        #remove parsed file
        os.remove(eachFile)

        print("old file name:",eachFile)
        newFile = eachFile[0:-1] + "4"
        print("new file name:",newFile)

        # write store procedure commands into files
        with open(newFile,"w") as fw:
            newCommand = DBCreate.generateCommandInsertServerSdr(fieldValueForStoreProcedure)
            #command = "DBCreate.storeProcedureInsertServerSdr("  + fieldValueForStoreProcedure + ")"
            print("\n\n\n==> command for write:",newCommand)
            fw.write(newCommand)
