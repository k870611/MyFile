USE server_management;
DROP PROCEDURE IF EXISTS insert_server_sdr_list_json;

DELIMITER //
CREATE PROCEDURE insert_server_sdr_list_json(IN var_insert_time VARCHAR(20), IN var_server_id VARCHAR(11), IN var_result json)
BEGIN
  INSERT INTO server_management.server_sdr_list_json (insert_time, server_id, result) VALUES (var_insert_time, var_server_id, var_result);
END //

DELIMITER ;