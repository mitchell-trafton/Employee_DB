# EMPLOYEE_DB

A pair of python programs that can add employee information to a CSV file, 
and then load that CSV into an employee information database.

*This was a class project where I utilized Python's database connectivity
funtionality using ```pyodbc```, as well as CSV writing functionality.*

- **employee_db_input.py** allows for a user to enter information for an
  employee. Input can either be command line parameters or several lines of
  user input. Data is saved to **employee.csv**. See program's Usage statement for more details.
- **load_to_db.py** takes only one argument for a csv file to write to the database. Exports all rows that don't cause key issues on the DB server.
- **employee_db_setup.sql** (MSSQL) sets up the employee database, creating the neccessary tables. 

## Setup
- Make sure to run **employee_db_setup.sql** before running the python scripts to avoid any errors.

## Notes
- Only the employee table was set up with Python for this assignment. If you wish to insert data for other tables, either manually update the relevant CSV file and run **load_to_db.py**, or add the data directly through your DBMS.
- The SQL for this program was written for MSSQL, so it is recommended that you use that database software when running this.