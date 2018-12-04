USE server_management;
DROP PROCEDURE IF EXISTS Insert_server_sel_save_list;

DELIMITER //
CREATE PROCEDURE Insert_server_sel_save_list(IN var_insert_time VARCHAR(20), IN var_server_id VARCHAR(10), IN val_sensor_type VARCHAR(30), IN val_event_detail VARCHAR(30), IN var_sel_id VARCHAR(11), IN var_sel_day VARCHAR(32), IN var_sel_time VARCHAR(32), IN var_sel_name VARCHAR(128), IN var_sel_info VARCHAR(256), IN var_sel_tag VARCHAR(100))
BEGIN
  INSERT INTO server_management.server_sel_save_list (insert_time, server_id, sensor_type, event_detail, sel_id, sel_day, sel_time, sel_name, sel_description, sel_tag) VALUES (var_insert_time, var_server_id, val_sensor_type, val_event_detail, var_sel_id, var_sel_day, var_sel_time, var_sel_name, var_sel_info, var_sel_tag);
END //

DELIMITER ;