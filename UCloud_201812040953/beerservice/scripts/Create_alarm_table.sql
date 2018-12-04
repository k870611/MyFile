USE `server_management`;

DROP TABLE IF EXISTS `alarm`;

CREATE TABLE `alarm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `alarm_enable` tinyint(2) DEFAULT '1',
  `alarm_name` varchar(45) DEFAULT '',
  `alarm_description` varchar(250) DEFAULT '',
  `alarm_level` varchar(45) DEFAULT '',
  `alarm_condition` varchar(45) DEFAULT '0',
  `alarm_value` DECIMAL(10,4),
  `sensor_name` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
