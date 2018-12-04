USE `server_management`;

DROP TABLE IF EXISTS log;

CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `log_module` varchar(45) DEFAULT '',
  `log_level` varchar(45) DEFAULT '',
  `log_description` varchar(250) DEFAULT '',
  `insert_time` datetime DEFAULT NULL,
  `log_source` varchar(45) DEFAULT '',
  `log_user_account` varchar(100) DEFAULT '',
  `log_user_org` varchar(100) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
