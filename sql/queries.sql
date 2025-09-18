INNER JOIN TABLE employees AS e ON dept.department_id = e.department_id
WHERE e.salary > 65000;