USE server_management;

DROP TABLE IF EXISTS server_sel_save_list;

CREATE TABLE server_sel_save_list
(
	id INT(11) NOT NULL AUTO_INCREMENT,
	insert_time DATETIME DEFAULT NULL,
	sensor_type VARCHAR(30) NOT NULL,
	event_detail VARCHAR(30) NOT NULL,
	server_id INT(11) NOT NULL,
	sel_id VARCHAR(11) NOT NULL,
	sel_day VARCHAR(32) NOT NULL,
	sel_time VARCHAR(32) NOT NULL,	
	sel_name VARCHAR(128) NOT NULL,
	sel_description VARCHAR(256) NOT NULL,
	sel_tag VARCHAR(100) DEFAULT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8; 