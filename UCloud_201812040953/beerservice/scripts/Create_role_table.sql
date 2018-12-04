USE `server_management`;

DROP TABLE IF EXISTS role;

CREATE TABLE `role` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role_name` varchar(45) DEFAULT '',
  `role_description` varchar(250) DEFAULT '',
  `role_group` varchar(45) DEFAULT '',
  `role_auth` int(11) DEFAULT '2',
  `role_server` tinyint(2) DEFAULT '1',
  `role_event` tinyint(2) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
