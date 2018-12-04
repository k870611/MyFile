USE server_management;
delimiter //

DROP EVENT IF EXISTS Scavenger //

SET @tomorrow = timestampadd(minute, 1, DATE(NOW())) //

CREATE EVENT Scavenger
ON SCHEDULE EVERY 1 hour starts @tomorrow
DO BEGIN

	DECLARE finish INT DEFAULT 0;
	DECLARE tab VARCHAR(100);
    DECLARE cur_tables CURSOR FOR
		SELECT A.table_name
		  FROM information_schema.tables A
		 INNER JOIN information_schema.columns B ON (A.table_name = B.table_name)
		 WHERE A.table_schema = 'server_management'
		   AND A.table_type = 'base table'
		   AND A.table_name <> 'log'
		   AND B.column_name = 'insert_time';
	DECLARE CONTINUE handler FOR NOT FOUND SET finish = 1;

    SET @expiretime = timestampadd(hour, -1, NOW());

	OPEN cur_tables;

my_loop:LOOP
		FETCH cur_tables INTO tab;
		IF finish = 1 THEN
			leave my_loop;
		END IF;

		SET @str = CONCAT('delete from ', tab, ' where insert_time < \'' , @expiretime , '\'');

		PREPARE stmt FROM @str;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
	END LOOP;

	CLOSE cur_tables;
END //
delimiter ;