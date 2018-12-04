
USE server_management;

DELIMITER //
DROP PROCEDURE IF EXISTS insert_server_arp_ex//

CREATE PROCEDURE `insert_server_arp_ex`(IN var_mac VARCHAR(45), IN var_ip VARCHAR(45))
BEGIN

	IF (SELECT count(*) FROM `server_info` WHERE var_mac IS NOT NULL AND STRCMP(server_mac, var_mac)=0)>0 THEN
		BEGIN
			UPDATE server_info SET server_ip=var_ip WHERE (var_mac IS NOT NULL AND STRCMP(server_mac, var_mac)=0) AND (server_ip IS NULL OR STRCMP(server_ip, var_ip)<>0);
		END;
	ELSE
		BEGIN
			IF (SELECT count(*) FROM `server_info` WHERE STRCMP(server_ip, var_ip)=0)>0 THEN
				BEGIN
					UPDATE `server_info` SET server_mac=var_mac WHERE (var_ip IS NOT NULL) AND STRCMP(server_ip, var_ip)=0;
				END;
			ELSE
				BEGIN
					UPDATE `server_info` SET server_mac=var_mac, server_ip=var_ip WHERE id=(SELECT id FROM `server_info` WHERE server_mac='' AND server_ip='' order by id limit 1);
				END;
			END IF;
		END;
	END IF;
	
END //

DELIMITER ;
