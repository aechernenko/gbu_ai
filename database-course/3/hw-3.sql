-- База данных «Сотрудники»:

-- 1. Выбрать среднюю зарплату по отделам.

SELECT 
    dept_name, 
	AVG(salary) AS avg_salary
FROM
    dept_emp de
        LEFT JOIN
    departments d ON d.dept_no = de.dept_no
        LEFT JOIN
    salaries s ON s.emp_no = de.emp_no
GROUP BY dept_name
;

-- 2. Выбрать максимальную зарплату у сотрудника.

SELECT 
    CONCAT(first_name, ' ', last_name) AS 'Name',
    MAX(salary) AS Salary
FROM
    employees e
        JOIN
    salaries s ON e.emp_no = s.emp_no
;

-- 3. Удалить одного сотрудника, у которого максимальная зарплата.

DELETE 
FROM 
	employees e 
WHERE 
	e.emp_no = 
		(SELECT 
			s.emp_no 
		 FROM 
			salaries s 
		 WHERE 
			s.salary = 
				(SELECT 
					MAX(salary) 
				 FROM 
					salaries s))
;

-- 4. Посчитать количество сотрудников во всех отделах.

SELECT 
    COUNT(emp_no) AS count
FROM
    dept_emp
;

-- 5. Найти количество сотрудников в отделах и посмотреть, сколько всего денег получает отдел.

SELECT 
    dept_name, COUNT(de.emp_no) AS 'count', SUM(salary) AS 'salary'
FROM
    dept_emp de
        LEFT JOIN
    departments d ON d.dept_no = de.dept_no
        LEFT JOIN
    salaries s ON s.emp_no = de.emp_no
GROUP BY dept_name
;