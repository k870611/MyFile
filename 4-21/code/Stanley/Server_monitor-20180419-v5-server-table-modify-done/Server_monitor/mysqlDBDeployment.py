import pymysql, time, os, json

class mysqlDBDeployment():
    def __init__(self):
        print("mysqlDBDeployment started")

    def buildDatabase(self,DBName):
        db = pymysql.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="123456"  # your password
                            )        # name of the data base

        cur = db.cursor()

        # create database
        print("Create database server_management...")

        dbCreateCommand = "create database " + DBName
        cur.execute(dbCreateCommand)
        time.sleep(1)
        
        db.commit()
        db.close()

    def buildTables(self,DBName,TableName,fieldDefinition):
        db = pymysql.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="123456",  # your password
                             db=DBName)        # name of the data base
        # example command:  mysql --user=root --password=$PASSWORD -D server_management --execute="CREATE TABLE server (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,server_id INT(11),server_slot VARCHAR(45),server_ip VARCHAR(45),server_mac VARCHAR(45),server_status INT(11),server_tag VARCHAR(45),server_power VARCHAR(45),server_power_detail VARCHAR(250),server_degree VARCHAR(45),server_degree_detail VARCHAR(250),server_note VARCHAR(250),server_update_time VARCHAR(250),signup_date DATE)"



        cur = db.cursor()
        sqlCommand = "CREATE TABLE " + TableName + fieldDefinition
        print("create command:",sqlCommand) 
        cur.execute(sqlCommand)
        time.sleep(1)

        db.commit()
        db.close()


    def insertData(self,DBName,TableName,fieldName,fieldValue):
        db = pymysql.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="123456",  # your password
                             db=DBName)        # name of the data base

        cur = db.cursor()
        sqlCommand =  "INSERT INTO " + TableName + " " + fieldName + " VALUES " + fieldValue
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

        for row in cur.fetchall():
            print(row)

        time.sleep(1)
        db.commit()

        db.close()

    def testStoreProcedure(self,DBName,TableName,fieldName,fieldValue):
        db = pymysql.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="dc2018_BMC",  # your password
                             db=DBName)        # name of the data base

        cur = db.cursor()
        sqlCommand =  "USE " + DBName + ";"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)
        
#        for row in cur.fetchall():
#            print(row)

        sqlCommand =  "CALL show_servers();"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

        for row in cur.fetchall():
            print(row)

        time.sleep(1)
#        db.commit()

        db.close()

    def storeProcedureShow(self,DBName,TableName,fieldName,fieldValue):
        db = pymysql.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="123456",  # your password
                             db=DBName)        # name of the data base

        cur = db.cursor()
        sqlCommand =  "USE " + DBName + ";"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

#        for row in cur.fetchall():
#            print(row)

        sqlCommand =  "CALL show_servers();"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

        for row in cur.fetchall():
            print(row)

        time.sleep(1)
#        db.commit()

        db.close()

    # store data into databases
    def storeProcedureInsertServerSdr(self,DBName,TableName,fieldValue):
        db = pymysql.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="123456",  # your password
                             db=DBName)        # name of the data base

        cur = db.cursor()
        sqlCommand =  "USE " + DBName + ";"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

#        for row in cur.fetchall():
#            print(row)

        valueString = ""
        valueList = list()
        valueList = fieldValue.split(';')
        valueNum = len(valueList)
        index = 1
        print("value num:",valueNum)
        print("field values:",valueList)
        for item in valueList:
            print("values:",item)
            valueString += item
            if index < valueNum:
                valueString += ","
            index += 1

        print("final values to be inserted:",valueString)


        sqlCommand =  "CALL insert_tables_server_sdr(" + valueString + ");"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

        for row in cur.fetchall():
            print(row)

        time.sleep(1)
        db.commit()

        db.close()



    def storeProcedureInsertServerSdrNoModification(self,DBName,TableName,fieldValue):
        db = pymysql.connect(host="localhost",    # your host, usually localhost
                             user="root",         # your username
                             passwd="123456",  # your password
                             db=DBName)        # name of the data base

        cur = db.cursor()
        sqlCommand =  "USE " + DBName + ";"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

#        for row in cur.fetchall():
#            print(row)

        valueString = ""
        valueList = list()
        valueList = fieldValue.split(';')
        valueNum = len(valueList)
        index = 1
        print("value num:",valueNum)
        print("field values:",valueList)
        for item in valueList:
            print("values:",item)
            valueString += item
            if index < valueNum:
                valueString += ","
            index += 1

        print("final values to be inserted:",valueString)


        sqlCommand =  "CALL insert_tables_server_sdr(" + valueString + ");"
        print("command:",sqlCommand)
        cur.execute(sqlCommand)

        for row in cur.fetchall():
            print(row)

        time.sleep(1)
        db.commit()

        db.close()



    def generateCommandInsertServerSdr(self,fieldValue):

        valueString = ""
        valueList = list()
        valueList = fieldValue.split(';')
        valueNum = len(valueList)
        index = 1
        print("value num:",valueNum)
        print("field values:",valueList)
        for item in valueList:
            print("values:",item)
            valueString += item
            if index < valueNum:
                valueString += ","
            index += 1

        print("final values to be inserted:",valueString)


        sqlCommand =  "CALL insert_tables_server_sdr(" + valueString + ");"
        print("command:",sqlCommand)

        return sqlCommand



    def replaceDataQuotation(self,data):
        print("\n\n\nnew string before replace:",data)
        #newString.replace(\', \")
        print("char num in string:",len(data))
        index = 0
        testString = ""
        for char in data:
            if data[index] == "'":
                #print("char\' found",char)

                testString += "\""
            else:
                #print("normal char:",char)
                testString += char
            index += 1

        print("\n\n\n new string:",testString)
        testString += '''}' '''

        print("\n\n\n=> new string:",testString)
#        finalString = newSdrInfo + testString
        print("final string:",testString)

        return testString

    def encapsulationCommand(self,data):
        print("\n\n\nnew string before replace:",data)
        #newString.replace(\', \")
        SdrHeader = '''NULL; CURRENT_TIMESTAMP;'1';'{"sdr list":'''
        finalCommand = SdrHeader + data
        print("command string:",(finalCommand))

        return finalCommand


