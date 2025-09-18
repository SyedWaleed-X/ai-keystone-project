INSERT INTO departments (department_name) VALUES ('Sales');
INSERT INTO departments (department_name) VALUES ('Engineering');
INSERT INTO departments (department_name) VALUES ('Human Resources');
INSERT INTO departments (department_name) VALUES ('Strategy');


INSERT INTO employees (name, hire_date, salary, department_id)
VALUES ('John Smith', '2024-03-15', 70000, 1);

INSERT INTO employees (name, hire_date, salary, department_id)
VALUES ('Jane Doe', '2023-11-20', 80000, 2);

INSERT INTO employees (name, hire_date, salary, department_id)
VALUES ('Emily Davis', '2022-06-10', 60000, 3);

INSERT INTO employees (name, hire_date, salary, department_id)
VALUES ('Emily Davis', '2022-06-10', 60000, NULL);

-- Assuming Jane Doe has employee id = 2
INSERT INTO projects (project_name, employee_id) VALUES ('Q4 Initiative', 2);

-- Assuming John Smith has employee id = 1
INSERT INTO projects (project_name, employee_id) VALUES ('Alpha Launch', 1);

UPDATE projects
SET employee_id = 1  -- Assign John Smith (id=1)
WHERE project_name = 'Q4 Initiative';