import sys
import os
import subprocess
import json
import time
import datetime

ACCOUNT = "admin"
PASSWORD = "admin"
# position of "id" of table columes
index_value = 1

def server_query():
    global ACCOUNT
    global PASSWORD


    TARGET = "'slot1'"
    mysqlCmd = 'mysql --user=root --password=dc2018_BMC -D server_management --execute="SELECT server_id FROM server "'
    print "cmd:",mysqlCmd

#    redfishCmd = "curl -k -u Administrator:superuser -X " + ACTION + " -H 'Content-Type:application/json' https://" + sp.str_bmc_static_ip + REDFISH_ENTRY
    results =os.popen(mysqlCmd).read()
    print "results:\n",results

    new_result = results.split()
    print "new result:",new_result
    # get current columes in table server
    new_list = new_result[1:]
    print "new list:",new_list

    #query individual colume from mysql
    global_table_dict = dict()


    server_ip_and_mac_dict = dict()

    mysqlCmd = 'mysql --user=root --password=dc2018_BMC -D server_management --execute="SELECT * FROM server "'
    print "cmd:",mysqlCmd

#    redfishCmd = "curl -k -u Administrator:superuser -X " + ACTION + " -H 'Content-Type:application/json' https://" + sp.str_bmc_static_ip + REDFISH_ENTRY
    results =os.popen(mysqlCmd).read()
    print "results2:\n",results
    new_result = results.split("\n")
    print "new_results2:",new_result



    for item in new_result:
        print "item 0:",item
        if item == "":
            print "line is null"
        else:
            new_line = item.split()
            print "new_line:",new_line

            if new_line[0] == "id":
                print "index line"
            else:

                temp_dict = dict()
                temp_dict['ip'] = new_line[3]
                temp_dict['mac'] = new_line[4]
                print "temp_dict:",temp_dict

                server_ip_and_mac_dict[new_line[0]] = temp_dict

    print "server ip and mac mapping:",server_ip_and_mac_dict



    COL_TARGET = "server_ip"
    mysqlCmd = 'mysql --user=root --password=dc2018_BMC -D server_management --execute="SELECT ' + COL_TARGET + ' FROM server "'
    #print "cmd:",mysqlCmd
    col_results =os.popen(mysqlCmd).read()
    #print "results:\n",col_results
    new_col_results = col_results.split()
    #print "item 0:",new_col_results[0]
    #print "item 1:",new_col_results[1:]
    global_table_dict[new_col_results[0]] = new_col_results[1:]


#    print "dict:",global_table_dict

#    jsondata = json.loads(results)

#    print "dict ip:",global_table_dict['server_ip']



    query_with_ipmitool(global_table_dict,server_ip_and_mac_dict)

def query_with_ipmitool(global_table_dict,server_ip_and_mac_dict):
    global ACCOUNT
    global PASSWORD
    global index_value
    #query dynamic ipmi data

    sensor_table_to_be_checked_list = list()
    sensor_table_to_be_checked_dict = dict()
    for ip in global_table_dict['server_ip']:
#        print "ip:",ip
        ipmiCmd = 'ipmitool -H ' + ip + ' -U ' + ACCOUNT + ' -P ' + PASSWORD + ' sensor'
        #print "ipmi cmd:",ipmiCmd
        results =os.popen(ipmiCmd).read()

        newline = results.split("\n")
        #print "ipmi result:",newline

        #print "length of cmd result:",len(newline)
        if  len(newline) == 1:
            # connection to target ipmi does not exist
            print "ipmi connection error of target ip:",ip
        else:
            for item in newline:
                item = item.strip()

                newitem = item.split("|")
                #print "newitem:",newitem
                sensor_table_to_be_checked_list.append(newitem)


            for item2 in sensor_table_to_be_checked_list:
                key_striped = item2[0].strip()
                sensor_table_to_be_checked_dict[key_striped] = item2

#    print "sensor dict:",sensor_table_to_be_checked_dict
#    print "inlet:",sensor_table_to_be_checked_dict['Inlet_Temp']
#    print "inlet temp:",sensor_table_to_be_checked_dict['Inlet_Temp'][index_value]
            print "ready to update values"
            # update Inlet temperature
            update_mysql("server","server_ip",ip,"server_degree",sensor_table_to_be_checked_dict['Inlet_Temp'][index_value])

            # update total power
            update_mysql("server","server_ip",ip,"server_power",sensor_table_to_be_checked_dict['Total_Power'][index_value])



''' command examples: cmd: mysql --user=root --password=dc2018_BMC -D server_management --execute="UPDATE server SET server_degree =  27.000      WHERE server.server_slot = 'slot1' "
    update_mysql("server","server_slot",TARGET,"server_degree",sensor_table_to_be_checked_dict['Inlet_Temp'][index_value])
'''
def update_mysql(TARGET_Table,TARGET_Colume,TARGET_Value,colume_name_to_be_changed, colume_value_to_be_changed):
    print "colume name:",colume_name_to_be_changed
    print "colume value:",colume_value_to_be_changed
    # update data
    mysqlCmd = 'mysql --user=root --password=dc2018_BMC -D server_management --execute="UPDATE ' + TARGET_Table +' SET ' + colume_name_to_be_changed + ' = ' + colume_value_to_be_changed +' WHERE ' + TARGET_Table + '.' + TARGET_Colume + ' = ' + "'" + TARGET_Value + "'" + ' "'
    print "cmd:",mysqlCmd
    results =os.popen(mysqlCmd).read()
    

#    mysql --user=root --password=dc2018_BMC -D server_management --execute="UPDATE server SET server_status = '2' WHERE server.server_slot ='slot1';"
#    updateCmd = 'mysql --user=root --password=dc2018_BMC -D server_management --execute="UPDATE `potluck` SET `confirmed` = 'Y' WHERE `potluck`.`name` ='Sandy'"'



def main():
    print "main"
    print "sys len:", len(sys.argv)
    if(len(sys.argv) == 2):
        targetIP = sys.argv[1]
        print "IP:", targetIP
        testDump(targetIP)
    else:
        while(1):
            server_query()
            print "\n\n\n"
            print "================data updated at time================:",datetime.datetime.now()
            time.sleep(3)
            
    #    print "Please input IP in commands, Examples: python dump_RSD_data_to_dict.py 192.168.0.1"


if __name__ == "__main__":
    main()
