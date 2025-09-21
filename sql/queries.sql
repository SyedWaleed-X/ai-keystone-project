INNER JOIN TABLE employees AS e ON dept.department_id = e.department_id
WHERE e.salary > 65000;


With company_avg as (

    SELECT AVG(SALARY) as avg_salary from employees
)

SELECT
name,
salary

from employees

WHERE

salary > (
    SELECT avg_salary from company_avg
)

Select 
e.name,
e.salary,

(Select avg(e.salary) from employees e) as avg_company_salary,

e.salary - (select avg(salary) from employees as e) as difference_from_avg

from employees as e


-- First, define the calculation and give it a name. It runs only ONCE.
WITH CompanyAverage AS (
    SELECT AVG(salary) as avg_sal FROM employees
)
-- Now, use the result as many times as you want in the main query.
SELECT
    e.name,
    e.salary,
    -- Usage #1: Displaying the pre-calculated average.
    ca.avg_sal AS company_average,
    -- Usage #2: Using the pre-calculated average in a calculation.
    e.salary - ca.avg_sal AS difference_from_average
FROM
    employees AS e, CompanyAverage AS ca; -- A simple way to join a single-value CTE




SELECT
    e.name,
    d.department_name,
    e.salary,
    -- This calculates the total for the 'partition' (the department)
    -- and pastes it on every row within that partition.
    SUM(e.salary) OVER (PARTITION BY d.department_name) AS department_total_salary,
    -- Now we can perform the percentage calculation using the two values.
    -- We multiply by 100.0 to ensure decimal division.
    (e.salary * 100.0 / SUM(e.salary) OVER (PARTITION BY d.department_name)) AS percentage_of_dept_total
FROM
    employees AS e
JOIN
    departments AS d ON e.department_id = d.id;


    



select 


p.project_name,
e.name as team_member_name,

CASE

when p.employee_id = e.id then 'Project Lead'

else 'Team member'

end as role


from projects as p

join

project_assignments as pa on p.project_id = pa.project_id

join

employees as e on e.id = pa.employee_id



-- for selecting all employyes from engineering department, and showing which projects 
-- they are working on, if any 


with eng_emps as (

select


e.id,
e.name,
d.department_name

from employees as e

join departments as d on d.id = e.department_id

where d.department_name = 'Engineering'
)

select 

e.name,
e.id,
e.department_name,
pa.project_id,
p.project_name
from eng_emps as e

join project_assignments as pa on pa.employee_id = e.id

join projects as p on p.project_id = pa.project_id


--- query that ranks employees based on their salary within their department


select

e.name,
e.salary,
d.department_name,
DENSE_RANK() OVER (PARTITION by department_id ORDER BY SALARY desc)

from employees as e

join departments as d on e.department_id = d.id



-- query that shows each employees salary and the department's total salary and how much % is the employees salary of the department's total



select

e.name,
e.salary,
d.department_name,

SUM(e.salary) over (PARTITION BY d.department_name) as dept_total_salary,


(e.salary *100/ SUM(e.salary) over (partition by d.department_name)) as percetange_of_dept_total
from employees as e

join departments as d on e.department_id = d.id


-- query which tells u salary rank of the employee 


with secondrank as  (

select 
e.name,
e.salary,
RANK() OVER (order by salary desc) as rank

from employees as e



)

select

e.name,
e.salary





from secondrank as e

where  rank = 2


-- query for combining cte and window function , employe and their dept and ranked by hiredate

with emp_dept as (

select
e.name,
e.hire_date,
d.department_name
from employees as e

join departments as d on e.department_id = d.id

)

select 

name,
department_name,
hire_date,

DENSE_RANK() OVER( PARTITION BY department_name ORDER BY hire_date desc) 

from emp_dept 
