USE server_management;
DROP PROCEDURE IF EXISTS insert_server_sdr_list;

DELIMITER //
CREATE PROCEDURE insert_server_sdr_list(IN var_insert_time VARCHAR(20), IN var_server_id VARCHAR(10), IN var_sensor_name VARCHAR(64), IN var_sensor_value VARCHAR(32), IN var_sensor_status VARCHAR(10), var_pure_value VARCHAR(10), var_unit VARCHAR(10))
BEGIN

  INSERT INTO server_management.server_sdr_list (insert_time, server_id, sensor_name, sensor_value, sensor_status,  sensor_pure_value, sensor_unit) VALUES (var_insert_time, var_server_id, var_sensor_name, var_sensor_value, var_sensor_status, var_pure_value, var_unit);

END //

DELIMITER ;
