USE `server_management`;

DROP TABLE IF EXISTS event;

CREATE TABLE `event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `event_type` int(11)  DEFAULT 1,
  `event_level` varchar(45) DEFAULT '',
  `event_name` varchar(200) DEFAULT '',
  `event_description` varchar(250) DEFAULT '',
  `event_time` varchar(45) DEFAULT '',
  `event_action` varchar(250) DEFAULT '',
  `sensor_type` varchar(30) DEFAULT NULL,
  `server_id` int(11) DEFAULT NULL,
  `sel_id` int(11) DEFAULT NULL,

  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
