USE server_management;

DELETE FROM role;

INSERT INTO role VALUES
 (1,'Manager','Kylin Manager','KyLin Group',1,1,1),
 (2,'Operator','Kylin Operator','KyLin Group',2,1,1),
 (3,'Viewer','Kylin Viewer','KyLin Group',3,1,0);


DELETE FROM acc_management;

INSERT INTO acc_management VALUES
 (1,'Admin','System Administrator','admin','','Admin@foxconn.com','',1,'',0,'2018-05-09 13:18:30',1),
 (2,'Demo','demo','demo','Default Organization1','demo@gmail.com','0999999999',1,'',0,'2018-04-25 16:22:19',2),
 (3,'Scheduler','Scheduler','scheduler','','Scheduler@foxconn.com','',1,'',0,'2018-04-14 09:17:57',2),
 (4,'Supervisor','System Supervisor','supervisor','','Supervisor@foxconn.com','',0,'2018-03-13 ~ 2018-03-14',0,'2018-04-14 09:17:57',2),
 (5,'kyLin','kyLin','kyLin1234','Default Organization1','kyLin@foxconn.com','0912345678',1,'',0,'2018-05-04 09:27:17',1);
