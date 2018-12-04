USE server_management;
DELIMITER //

DROP TABLE IF EXISTS server_sel_save_json;

CREATE TABLE server_sel_save_json 
(
	ID INT(11) NOT NULL AUTO_INCREMENT,
	insert_time DATETIME DEFAULT NULL,
	server_id INT(11) NOT NULL,
	result JSON DEFAULT NULL,
	PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 //

DELIMITER ;