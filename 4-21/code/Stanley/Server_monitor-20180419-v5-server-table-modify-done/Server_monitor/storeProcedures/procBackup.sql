USE server_management;
DROP PROCEDURE IF EXISTS insert_tables;

DELIMITER //
CREATE PROCEDURE insert_tables_server_sdr(IN var1 VARCHAR(1000),IN var2 VARCHAR(10000), IN var3 VARCHAR(10000), IN var4 VARCHAR(10000), IN var5 VARCHAR(10000), IN var6 VARCHAR(10000), IN var7 json)
BEGIN
  INSERT INTO server_management.server_sdr VALUES (var1,var2,var3,var4,var5,var6,var7);
END //

DELIMITER ;
