USE `server_management`;

DROP TABLE IF EXISTS acc_management;

CREATE TABLE `acc_management` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `acc_management_account` varchar(100) DEFAULT '',
  `acc_management_name` varchar(100) DEFAULT '',
  `acc_management_password` varchar(128) DEFAULT '',
  `acc_management_organization` varchar(100) DEFAULT '',
  `acc_management_email` varchar(100) DEFAULT '',
  `acc_management_phone` varchar(45) DEFAULT '',
  `acc_management_active` tinyint(2) DEFAULT '0',
  `acc_management_acc_deadline` varchar(45) DEFAULT '',
  `acc_management_org_manager` tinyint(2) DEFAULT '0',
  `acc_management_operate_date` datetime DEFAULT NULL,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `role_id_idx` (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
