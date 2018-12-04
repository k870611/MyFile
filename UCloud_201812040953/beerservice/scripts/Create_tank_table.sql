USE server_management;

DROP TABLE IF EXISTS tank;

CREATE TABLE `tank` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tank_name` varchar(100) DEFAULT 'tank',
  `tank_description` varchar(255) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
