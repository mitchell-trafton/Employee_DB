CREATE DATABASE employee_DB;
USE employee_DB;
GO

CREATE SCHEMA info;
GO

-- EMPLOYEE TABLE
CREATE TABLE info.employee(
    employee_id INT IDENTITY PRIMARY KEY, -- unique identifier for employee
    first_name VARCHAR(100) NOT NULL, -- employee's first name
    last_name VARCHAR(100) NOT NULL, -- employee's last name
    age INT NOT NULL, -- employee's age in years
    salary DECIMAL(10,2) NOT NULL, -- anual salary for employee
    manager_id INT, -- id of manager, FK to employee_id in another employee instance
    dept_id INT, -- id of department worked in, FK to dept_id in department
    addr_id INT, -- address where employee works, FK to addr_id in address

    FOREIGN KEY (manager_id) REFERENCES info.employee(employee_id)
);


-- DEPARTMENT TABLE
CREATE TABLE info.department (
    dept_id INT IDENTITY PRIMARY KEY, -- unique identifier for department
    name VARCHAR(50) NOT NULL, -- name of department
    manager_id INT NOT NULL, -- ID of manager of department, FK to employee_id in employee
    headqtr_addr_id INT NOT NULL, -- address of department's headquarters, FK to addr_id in address

    FOREIGN KEY (manager_id) REFERENCES info.employee(employee_id) 
);

-- ADDRESS TABLE
CREATE TABLE info.address(
    addr_id INT IDENTITY PRIMARY KEY, -- unique identifier for address
    street VARCHAR(150) NOT NULL, -- street address
    city VARCHAR(100) NOT NULL, -- city of address
    state CHAR(2) NOT NULL -- two-letter state of address
);

---- Add foreign key restraints

-- Add foreign key restraints for dept_id and addr_id in employee
ALTER TABLE info.employee ADD FOREIGN KEY (dept_id) REFERENCES info.department(dept_id);
ALTER TABLE info.employee ADD FOREIGN KEY (addr_id) REFERENCES info.address(addr_id);

-- Add foreign key restraint for headqtr_addr_id in department
ALTER TABLE info.department ADD FOREIGN KEY (headqtr_addr_id) REFERENCES info.address(addr_id);