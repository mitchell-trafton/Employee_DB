import csv
from numpy import NaN, float64, nan
import pyodbc
import sys
import pandas as pd

from table_type import Table
'''
This program takes data from employee.csv, department.csv, or address.csv, and inserts
its data into the proper table in employee_DB.

A command line argument of -emp, -dep, or -adr is used to specify the table/csv to use.
'''

# Initialize database connection
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost;" # <-- this might need to change depending on your local dbms name
                      "Database=employee_DB;"
                      "Trusted_Connection=yes;")



# vars
usage = ("Usage: -[emp | dep | adr]") # usage statement

data = pd.DataFrame()

tableSelect = Table # table object representing selected table to insert into

badKeyFail = [] # table containing IDs of records that couldn't be inserted due to duplicate primary keys or foreign keys not having a matching counterpart

otherFail = [] # table containing IDs of records that couldn't be inserted due to an error besides duplicate primary keys



# verify that user passed correct command line parameter
if len(sys.argv) == 2 and sys.argv[1] in ['-emp', '-dep', '-adr']:
    
    if sys.argv[1] == '-emp': tableSelect = Table.EMPLOYEE
    elif sys.argv[1] == '-dep': tableSelect = Table.DEPARTMENT
    elif sys.argv[1] == '-adr': tableSelect = Table.ADDRESS

else:
    exit(f"Error: Command line arguments missing or unrecognized.\n\n{usage}")



# extract data from desired table to dataframe
try:
    data = pd.read_csv(f'{tableSelect.name.lower()}.csv')
except: exit(f"Error: Unable to read from {tableSelect.name.lower()}.csv."
             " Please verify that the file isn't empty and"
             " that it exists and is accessable by you in the current directory.")



# export to database
cursor = cnxn.cursor()

#build sql query
if tableSelect == Table.EMPLOYEE: # employee table
    # turn IDENTITY_INSERT on for employee table on server to allow custom employee_id's to be inserted 
    cursor.execute('SET IDENTITY_INSERT info.employee ON')

    for r in range(data.shape[0]):
        query = ("insert into info.employee (employee_id, first_name, last_name, age, salary, manager_id, dept_id, addr_id) values "
                 f"({data['employee_id'][r]}, "
                 f"'{data['first_name'][r]}', "
                 f"'{data['last_name'][r]}', "
                 f"{data['age'][r]}, "
                 f"{data['salary'][r]}, "
                 f"{data['manager_id'][r] if not data['manager_id'].isna()[r] else 'NULL'}, "
                 f"{data['dept_id'][r] if not data['dept_id'].isna()[r] else 'NULL'}, "
                 f"{data['addr_id'][r] if not data['addr_id'].isna()[r] else 'NULL'})")

        try:# try to run quey
            cursor.execute(query)
        except pyodbc.IntegerityError:#primary key already exists
            badKeyFail.append(data['employee_id'][r])
        except: #data can't be inserted for other reason
            otherFail.append(data['employee_id'][r])


elif tableSelect == Table.DEPARTMENT: # department table
    # turn IDENTITY_INSERT on for department table on server to allow custom dept_id's to be inserted 
    cursor.execute('SET IDENTITY_INSERT info.department ON')

    for r in range(data.shape[0]):
        query = ("insert into info.department (dept_id, name, manager_id, headqtr_addr_id) values "
                 f"({data['dept_id'][r]}, "
                 f"'{data['name'][r]}', "
                 f"{data['manager_id'][r]}, "
                 f"{data['headqtr_addr_id'][r]})")

        try:# try to run quey
            cursor.execute(query)
        except pyodbc.IntegrityError:#primary key already exists
            badKeyFail.append(data['dept_id'][r])
        except: #data can't be inserted for other reason
            otherFail.append(data['dept_id'][r])


elif tableSelect == Table.ADDRESS: # address table
    # turn IDENTITY_INSERT on for address table on server to allow custom addr_id's to be inserted 
    cursor.execute('SET IDENTITY_INSERT info.addr ON')

    for r in range(data.shape[0]):
        query = ("insert into info.address (addr_id, street, city, state) values "
                 f"({data['addr_id'][r]}, "
                 f"'{data['street'][r]}', "
                 f"'{data['city'][r]}', "
                 f"'{data['state'][r]}')")

        try:# try to run quey
            cursor.execute(query)
        except pyodbc.IntegrityError:#primary key already exists
            badKeyFail.append(data['addr_id'][r])
        except: #data can't be inserted for other reason
            otherFail.append(data['addr_id'][r])



# print the IDs for any records that couldn't be inserted

if len(badKeyFail) > 0: #print IDs for records with bad primary/foreign keys
    print(f"The records with the following {tableSelect.name.lower()} IDs could not be inserted because "
          f"either the {tableSelect.name.lower()} ID already exists in the database, or any of the foreign keys not having a matching counterpart:")
    for bkf in badKeyFail: print(bkf)
    print()#newline

if len(otherFail) > 0: #print IDs for records having non-primary/forign key issues
    print(f"The records with the following {tableSelect.name.lower()} IDs could not be inserted:")
    for of in otherFail: print(of)
    print("This is likely due to improper formatting of data.\n")



# commit and close connection
cnxn.commit()
cursor.close()



exit("Database write finished.")