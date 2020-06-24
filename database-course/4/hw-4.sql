-- 1. Создать VIEW на основе запросов, которые вы сделали в ДЗ к уроку 3.
-- 2. Создать функцию, которая найдет менеджера по имени и фамилии.
-- 3. Создать триггер, который при добавлении нового сотрудника будет выплачивать ему вступительный бонус, занося запись об этом в таблицу salary.


--ЗАДАЧА № 1: Создать VIEW на основе запросов, которые вы сделали в ДЗ к уроку 3.

-- База данных «Сотрудники»:

-- 1. Выбрать среднюю зарплату по отделам.

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `task_1` AS
    SELECT 
        `d`.`dept_name` AS `dept_name`,
        AVG(`s`.`salary`) AS `avg_salary`
    FROM
        ((`dept_emp` `de`
        LEFT JOIN `departments` `d` ON ((`d`.`dept_no` = `de`.`dept_no`)))
        LEFT JOIN `salaries` `s` ON ((`s`.`emp_no` = `de`.`emp_no`)))
    GROUP BY `d`.`dept_name`

-- 2. Выбрать максимальную зарплату у сотрудника.

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `task_2` AS
    SELECT 
        CONCAT(`e`.`first_name`, ' ', `e`.`last_name`) AS `Name`,
        MAX(`s`.`salary`) AS `Salary`
    FROM
        (`employees` `e`
        JOIN `salaries` `s` ON ((`e`.`emp_no` = `s`.`emp_no`)))

-- 4. Посчитать количество сотрудников во всех отделах.
	
CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `task_4` AS
    SELECT 
        COUNT(`dept_emp`.`emp_no`) AS `count`
    FROM
        `dept_emp`
		
-- 5. Найти количество сотрудников в отделах и посмотреть, сколько всего денег получает отдел.

CREATE 
    ALGORITHM = UNDEFINED 
    DEFINER = `root`@`localhost` 
    SQL SECURITY DEFINER
VIEW `task_5` AS
    SELECT 
        `d`.`dept_name` AS `dept_name`,
        COUNT(`de`.`emp_no`) AS `count`,
        SUM(`s`.`salary`) AS `salary`
    FROM
        ((`dept_emp` `de`
        LEFT JOIN `departments` `d` ON ((`d`.`dept_no` = `de`.`dept_no`)))
        LEFT JOIN `salaries` `s` ON ((`s`.`emp_no` = `de`.`emp_no`)))
    GROUP BY `d`.`dept_name`

-- ЗАДАЧА № 2: Создать функцию, которая найдет менеджера по имени и фамилии.
	
USE `employees`;
DROP procedure IF EXISTS `get_manager_number`;

DELIMITER $$
USE `employees`$$
CREATE PROCEDURE `get_manager_number` (first_name_param VARCHAR(14), last_name_param VARCHAR(16), OUT emp_no_param INT)
BEGIN
SELECT emp_no INTO emp_no_param
FROM employees
WHERE (first_name = first_name_param) AND (last_name = last_name_param);
END$$

DELIMITER ;