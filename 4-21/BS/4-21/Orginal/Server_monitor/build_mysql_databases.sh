if [ $# -lt 1 ];then
        echo "too few argument"
        echo "example: build_mysql_databases.sh PASSWORD_OF_Mysql"
        exit 1
fi
# default password:dc2018_BMC
PASSWORD=$1
echo $1

echo "Start creating databases server_management"
mysql --user=root --password=$PASSWORD  --execute="create database server_management"

sleep 1

echo "create table server"
mysql --user=root --password=$PASSWORD -D server_management --execute="CREATE TABLE server (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,server_id INT(11),server_slot VARCHAR(45),server_ip VARCHAR(45),server_mac VARCHAR(45),server_status INT(11),server_tag VARCHAR(45),server_power VARCHAR(45),server_power_detail VARCHAR(250),server_degree VARCHAR(45),server_degree_detail VARCHAR(250),server_note VARCHAR(250),server_update_time VARCHAR(250),signup_date DATE)"

sleep 1


echo "insert basic data into server"
mysql --user=root --password=$PASSWORD -D server_management --execute="INSERT INTO server (id,server_id,server_slot,server_ip,server_mac,server_status,server_tag,server_power,server_power_detail,server_degree,server_degree_detail,server_note,server_update_time,signup_date) VALUES (NULL, '1','slot1','192.168.16.201','30:0E:D5:FF:17:56','1','Foxconn','80','800W Delta power','35','Inlet Sensor','Ali Chilin','2018-04-03','2018-04-03')"

sleep 1


echo "insert basic data into server"
mysql --user=root --password=$PASSWORD -D server_management --execute="INSERT INTO server (id,server_id,server_slot,server_ip,server_mac,server_status,server_tag,server_power,server_power_detail,server_degree,server_degree_detail,server_note,server_update_time,signup_date) VALUES (NULL, '2','slot2','192.168.16.202','30:0E:D5:FF:17:60','1','Foxconn','80','800W Delta power','36','Inlet Sensor','Ali Chilin','2018-04-03','2018-04-03')"

sleep 1

################################################
#build table server_sdr
echo "create table server_sdr"
mysql --user=root --password=$PASSWORD -D server_management --execute="CREATE TABLE server_sdr (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,server_sdr_id INT(11),server_sdr_name VARCHAR(45),server_sdr_status VARCHAR(45),server_sdr_value VARCHAR(45),server_id INT(11))"

sleep 1

echo "insert data into server_sdr"
mysql --user=root --password=$PASSWORD -D server_management --execute="INSERT INTO server_sdr (id,server_sdr_id,server_sdr_name,server_sdr_status,server_sdr_value,server_id) VALUES (NULL, '1','CPU0_Temp','ok','48.000','1')"

sleep 1

#build table server_lan
echo "create table server_lan"
mysql --user=root --password=$PASSWORD -D server_management --execute="CREATE TABLE server_lan (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,server_lan_id INT(11),server_lan_name VARCHAR(45),server_lan_value VARCHAR(45),server_id INT(11))"

sleep 1

#build table server_fru
echo "create table server_fru"
mysql --user=root --password=$PASSWORD -D server_management --execute="CREATE TABLE server_fru (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,server_fru_id INT(11),server_fru_name VARCHAR(45),server_fru_value VARCHAR(45),server_id INT(11))"

sleep 1

