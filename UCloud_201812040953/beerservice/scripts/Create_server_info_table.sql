USE `server_management`;

DROP TABLE IF EXISTS server_info;

CREATE TABLE `server_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_slot` int(11) DEFAULT '0',
  `server_ip` varchar(45) DEFAULT '',
  `server_mac` varchar(45) DEFAULT '',
  `server_update_time` varchar(45) DEFAULT '',
  `server_account` varchar(100) DEFAULT '',
  `server_password` varchar(128) DEFAULT '',
  `server_active` tinyint(2) DEFAULT '1',
  `tank_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tank_id_idx` (`tank_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
