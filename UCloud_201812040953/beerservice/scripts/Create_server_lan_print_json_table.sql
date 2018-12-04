USE server_management;
DELIMITER //

DROP TABLE IF EXISTS server_lan_print_json;

CREATE TABLE server_lan_print_json 
(
	id INT(11) NOT NULL AUTO_INCREMENT,
	insert_time DATETIME DEFAULT NULL,
	server_id INT(11) NOT NULL,
	result JSON DEFAULT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 //

DELIMITER ;