USE server_management;
DROP VIEW IF EXISTS sensor_alarm;

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `server_management`.`sensor_alarm` AS
    SELECT 
        `s`.`id` AS `id`,
        `s`.`insert_time` AS `insert_time`,
        `s`.`server_id` AS `server_id`,
        `s`.`sensor_name` AS `sensor_name`,
        `s`.`sensor_value` AS `sensor_value`,
        `s`.`sensor_status` AS `sensor_status`,
        `s`.`sensor_pure_value` AS `sensor_pure_value`,
        `s`.`sensor_unit` AS `sensor_unit`,
        `a`.`id` AS `alarmid`,
        `a`.`alarm_name` AS `alarm_name`,
        `a`.`alarm_description` AS `alarm_description`,
        `a`.`alarm_level` AS `alarm_level`
    FROM
        ((((SELECT 
            `server_management`.`server_sdr_list_json`.`server_id` AS `server_id`,
                MAX(`server_management`.`server_sdr_list_json`.`insert_time`) AS `insert_time`
        FROM
            `server_management`.`server_sdr_list_json`
        GROUP BY `server_management`.`server_sdr_list_json`.`server_id`)) `b`
        LEFT JOIN `server_management`.`server_sdr_list` `s` ON (((`s`.`insert_time` = `b`.`insert_time`)
            AND (`s`.`server_id` = `b`.`server_id`))))
        JOIN `server_management`.`alarm` `a` ON ((`a`.`sensor_name` = `s`.`sensor_name`)))
    WHERE
        ((`a`.`alarm_enable` = 1)
            AND (`a`.`sensor_name` = `s`.`sensor_name`)
            AND (((`a`.`alarm_condition` = '>')
            AND (`a`.`alarm_value` > `s`.`sensor_pure_value`))
            OR ((`a`.`alarm_condition` = '>=')
            AND (`a`.`alarm_value` >= `s`.`sensor_pure_value`))
            OR ((`a`.`alarm_condition` = '<')
            AND (`a`.`alarm_value` < `s`.`sensor_pure_value`))
            OR ((`a`.`alarm_condition` = '<=')
            AND (`a`.`alarm_value` > `s`.`sensor_pure_value`))
            OR ((`a`.`alarm_condition` = '=')
            AND (`a`.`alarm_value` = `s`.`sensor_pure_value`))
            OR ((`a`.`alarm_condition` = '<>')
            AND (`a`.`alarm_value` <> `s`.`sensor_pure_value`))))