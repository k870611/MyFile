USE server_management;
DROP PROCEDURE IF EXISTS show_servers;

DELIMITER //
CREATE PROCEDURE show_servers()
BEGIN
  SELECT * FROM server_sdr;
END //

DELIMITER ;
