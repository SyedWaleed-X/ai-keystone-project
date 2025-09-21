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


-- We will insert multiple employees in a single, efficient statement.
-- The new IDs will be assigned automatically, starting from 5.
INSERT INTO employees (name, hire_date, salary, department_id) VALUES
('Michael Chen', '2023-01-05', 95000, 2),   -- ID: 5, Engineering
('Sarah Rodriguez', '2024-05-20', 68000, 1),  -- ID: 6, Sales
('David Kim', '2021-08-30', 110000, 2),  -- ID: 7, Engineering
('Laura Williams', '2023-09-01', 52000, 1),  -- ID: 8, Sales
('Chris Lee', '2024-02-12', 75000, 2),    -- ID: 9, Engineering
('Jessica Taylor', '2022-04-18', 48000, 3),   -- ID: 10, Human Resources
('Brian Miller', '2023-07-22', 130000, 4), -- ID: 11, Strategy
('Olivia Brown', '2024-01-15', 72000, 2);   -- ID: 12, Engineering


-- Let's assign some of our new employees as leads on new projects.
INSERT INTO projects (project_name, employee_id) VALUES
('Project Phoenix', 7),  -- David Kim (Senior Engineer) leads this
('Titan Migration', 5),    -- Michael Chen leads this
('Omega Protocol', 7),     -- David Kim also leads this second project
('Cost Reduction Initiative', 11); -- Brian Miller (Strategy) leads this