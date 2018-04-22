import pymysql, time, os, json
import parser.mysqlDBDeployment as mysqlDBDeployment


if __name__ == '__main__':
    DBCreate = mysqlDBDeployment.mysqlDBDeployment()

    DBName = "server_management"

    # build table - server_sdr
    TableName = "server_sdr"


    with open("/home/stanley/workspace/Server_monitor/logs/output-2-20180413165236.txt.3") as json_data:
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
    print("final command==>",fieldValueForStoreProcedure)
    DBCreate.storeProcedureInsertServerSdr(DBName,TableName,fieldValueForStoreProcedure)


    # write store procedure commands into files
    with open("/home/stanley/workspace/Server_monitor/logs/output-2-20180413165236.txt.4","w") as fw:
        newCommand = DBCreate.generateCommandInsertServerSdr(fieldValueForStoreProcedure)
        #command = "DBCreate.storeProcedureInsertServerSdr("  + fieldValueForStoreProcedure + ")"
        print("\n\n\n==> command for write:",newCommand)
        fw.write(newCommand)
