USE server_management;
DROP PROCEDURE IF EXISTS select_server_info_list;

DELIMITER //
CREATE PROCEDURE select_server_info_list()
BEGIN

	SELECT id, server_ip,server_account,server_password FROM server_info WHERE server_active=True;

END //

DELIMITER ;

