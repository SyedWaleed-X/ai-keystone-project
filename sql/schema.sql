
-- Table to store department information
create TABLE departments {
    id SERIAL PRIMARY KEY, -- Unique identifier for each department
    department_name VARCHAR(100) NOT NULL UNIQUE -- Name of the department (must be unique)
}


-- Table to store employee information
CREATE TABLE employees (
    id          SERIAL      PRIMARY KEY, -- Unique identifier for each employee
    name        VARCHAR(100) NOT NULL,   -- Employee's name
    hire_date   DATE,                    -- Date the employee was hired
    salary      INT,                     -- Employee's salary
    department_id INT REFERENCES departments(id) -- Reference to the department
);