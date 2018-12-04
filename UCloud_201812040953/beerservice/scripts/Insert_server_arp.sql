
USE server_management;
DROP PROCEDURE IF EXISTS insert_server_arp;

DELIMITER //
CREATE PROCEDURE `insert_server_arp`(IN var_mac VARCHAR(45), IN var_ip VARCHAR(45))
BEGIN

	IF (SELECT count(*) FROM `server_info` WHERE var_mac IS NOT NULL AND STRCMP(server_mac, var_mac)=0)>0 THEN
		BEGIN
			UPDATE server_info SET server_ip=var_ip WHERE (var_mac IS NOT NULL AND STRCMP(server_mac, var_mac)=0) AND (server_ip IS NULL OR STRCMP(server_ip, var_ip)<>0) AND server_active=1;
		END;
	ELSE
		BEGIN
			IF (SELECT count(*) FROM `server_info` WHERE STRCMP(server_ip, var_ip)=0)>0 THEN
				BEGIN
					UPDATE `server_info` SET server_mac=var_mac WHERE (var_ip IS NOT NULL) AND STRCMP(server_ip, var_ip)=0 AND server_active=1;
				END;
			END IF;
		END;
	END IF;
	
END //

DELIMITER ;
