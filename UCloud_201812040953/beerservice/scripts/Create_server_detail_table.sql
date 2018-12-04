USE `server_management`;

DROP TABLE IF EXISTS server_detail;

CREATE TABLE `server_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `server_tag` varchar(250) DEFAULT '',
  `server_note` varchar(250) DEFAULT '',
  `server_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
