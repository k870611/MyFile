USE server_management;
DELIMITER //

DROP TABLE IF EXISTS server_sdr_list;

CREATE TABLE server_sdr_list
(
	id INT(11) NOT NULL AUTO_INCREMENT,
	insert_time DATETIME DEFAULT NULL,
	server_id INT(11) NOT NULL,
	sensor_name VARCHAR(64) NOT NULL,
	sensor_value VARCHAR(32) NOT NULL,
	sensor_status VARCHAR(10) NOT NULL,	
	sensor_pure_value DECIMAL(10,4),
	sensor_unit VARCHAR(10),	
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 //

DELIMITER ;
