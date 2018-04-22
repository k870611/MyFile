import time, os
import mysqlDBDeployment as mysqlDBDeployment

if __name__ == '__main__':
    DBCreate = mysqlDBDeployment.mysqlDBDeployment()

    DBName = "server_management"
    TableName = "server"
    # create database - server_management
    print("Start to create database")
    DBCreate.buildDatabase(DBName)

    # build table - server
    print("Start to create table - server")

    fieldDefinition = " (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,timestamp DATETIME,server_id INT(11),results json DEFAULT NULL)"
    DBCreate.buildTables(DBName,TableName,fieldDefinition)

    
    #print("insert 1st basic data into server")
    #fieldName = '''(id,server_id,server_slot,server_ip,server_mac,server_status,server_tag,server_power,server_power_detail,server_degree,server_degree_detail,server_note,server_update_time,signup_date)'''
    #fieldValue = '''(NULL, '1','slot1','192.168.16.201','30:0E:D5:FF:17:56','1','Foxconn','80','800W Delta power','35','Inlet Sensor','Ali Chilin','2018-04-03','2018-04-03')'''
    #DBCreate.insertData(DBName,TableName,fieldName,fieldValue)


    #print("insert 2nd basic data into server")
    #fieldName = "(id,server_id,server_slot,server_ip,server_mac,server_status,server_tag,server_power,server_power_detail,server_degree,server_degree_detail,server_note,server_update_time,signup_date)"
    #fieldValue = "(NULL, '2','slot2','192.168.16.202','30:0E:D5:FF:17:60','1','Foxconn','80','800W Delta power','36','Inlet Sensor','Ali Chilin','2018-04-03','2018-04-03')"
    #DBCreate.insertData(DBName,TableName,fieldName,fieldValue)

    # build table - server_sdr
    '''
    TableName = "server_sdr"
    print("Start to create table - server_sdr")
    fieldDefinition = " (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,server_sdr_id INT(11),server_sdr_name VARCHAR(45),server_sdr_status VARCHAR(45),server_sdr_value VARCHAR(45),server_id INT(11),json_value json DEFAULT NULL)"
    DBCreate.buildTables(DBName,TableName,fieldDefinition)
    '''

    TableName = "server_sdr"
    print("Start to create table - server_sdr")
    fieldDefinition = " (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,timestamp DATETIME,server_id INT(11),results json DEFAULT NULL)"
    DBCreate.buildTables(DBName,TableName,fieldDefinition)

    '''
    print("insert 2nd basic data into  - server_sdr")
    fieldName = "(id,server_sdr_id,server_sdr_name,server_sdr_status,server_sdr_value,server_id)"
    fieldValue = "(NULL, '1','CPU0_Temp','ok','48.000','1')"
    DBCreate.insertData(DBName,TableName,fieldName,fieldValue)
    

    print("insert 2nd basic data into  - server_sdr")
    fieldName = "(id,timestamp,server_id,results)"
    fieldValue = "(NULL, CURRENT_TIMESTAMP,'1','{}')"
    DBCreate.insertData(DBName,TableName,fieldName,fieldValue)
    '''

    # build table - server_lan
    TableName = "server_lan"
    print("Start to create table - server_lan")
    fieldDefinition = " (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,timestamp DATETIME,server_id INT(11),results json DEFAULT NULL)"
    DBCreate.buildTables(DBName,TableName,fieldDefinition)

    # build table - server_fru
    TableName = "server_fru"
    print("Start to create table - server_fru")
    fieldDefinition = " (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,timestamp DATETIME,server_id INT(11),results json DEFAULT NULL)"
    DBCreate.buildTables(DBName,TableName,fieldDefinition)



