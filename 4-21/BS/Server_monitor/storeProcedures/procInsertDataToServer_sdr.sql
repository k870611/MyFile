USE server_management;
DROP PROCEDURE IF EXISTS insert_tables;

DELIMITER //
CREATE PROCEDURE insert_tables_server_sdr(IN var_id VARCHAR(1000),IN var_timestamp VARCHAR(10000), IN var_server_id VARCHAR(10000), IN var_result json)
BEGIN
  INSERT INTO server_management.server_sdr VALUES (var_id,var_timestamp,var_server_id,var_result);
END //

DELIMITER ;
