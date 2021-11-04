## PROGRAMMED BY MITCHELL TRAFTON

import csv
import sys
import os
import pyodbc
from typing import Union
from re import split
import pandas as pd

from table_type import Table

'''
This program takes in either a list of command line values or several lists of data
from user input, and inserts them into the appropriate csv file 
(employee.csv, department.csv, or address.csv) associated with a 
database table in employee_DB. 

For inserting via command line args, user enters '-emp', '-dep', or '-adr' to specity
either the employee, department, or address table, followed by the data items to put
into that table, minus id attributes. See usage statement for specifics. This is
good for if the user only has one data record to insert.

For inserting via user inputed lists, user eners only '-emp', '-dep', or '-adr' as
command line args to specify table, and is prompted to type comma separated lists 
for the data records. This is good for if the user wishes to insert multiple data records.

The program formats the data for insertion, checking for incompatibilities with
foreign keys, improper types, etc., and if everything is good, it is inserted into
the proper csv file.
'''

def validateInput(data:list, table:Table) -> Union[list, str]:
    '''
    Validates the inputed list containing data and verifies that it is correctly
    formatted for inserion into the table specified by 'table' (by both type 
    and number of variables). Returns a formatted list if everyghing is ok, and an
    error message string if not.

    Parameters:
    data  -> List containing data to verify wheather it would make a proper tuple
             in the specified table.
    table -> Table enum specifying which table in the employee_DB the input is meant for

    Output:
    List containing data that is properly formated if data from list is proper.
    Empty list if passed in data wasn't formatted properly.
    '''

    output = [] #list to be outputed
    
    try:
        if table == Table.EMPLOYEE:
            output.append(data[0]) #first name
            
            output.append(data[1]) #last name

            if data[2].isdigit(): #age
                output.append(int(data[2]))
            else:
                raise TypeError('age', data[2], 'integer')

            if data[3].isdecimal() and float(data[3]) < 10000000000: #salary
                output.append(float(data[3]))
            else:
                raise TypeError('salary', data[3], 'dollar value < $10B')
            
            if len(data) >= 5:
                if (data[4].isdigit() or data[4] == 'null'): #manager ID
                    output.append(int(data[4]) if data[4].isdigit() else 'null')
                else:
                    raise TypeError('manager_id', data[4], 'integer')
            
            if len(data) >= 6: 
                if (data[5].isdigit() or data[5] == 'null'): #department ID
                    output.append(int(data[5]) if data[5].isdigit() else 'null')
                else:
                    raise TypeError('dept_id',  data[5], 'integer')

            if len(data) >= 7:
                if (data[6].isdigit() or data[6] == 'null'): #address ID
                    output.append(int(data[6]) if data[6].isdigit() else 'null')
                else:
                    raise TypeError('addr_id',  data[6], 'integer')
            
        

        elif table == Table.DEPARTMENT:
            output.append(data[0]) #name

            if data[1].isdigit(): #manager ID
                output.append(int(data[1]))
            else:
                raise TypeError('manager_id', data[1], 'integer')

            if data[2].isdigit(): #headqtr_addr_id
                output.append(int(data[2]))
            else:
                raise TypeError('headqtr_addr_id', data[2], 'integer')
            


        elif table == Table.ADDRESS:
            output.append(data[0]) #street

            output.append(data[1]) #city

            if len(data[2]) == 2: #state
                output.append(data[2])
            else:
                raise TypeError('state' , data[2], 'two-letter string')


    except IndexError: return("Error: Number of parameters in incorrect for an entry in"
                           f" the {table.name.lower()} table.")
    
    except TypeError as te: return(f"Error: Parameter '{te.args[0]}' cannot be " 
                                  f"'{te.args[1]}'. Expecting {te.args[2]}.")

    return output
## END VALIDATEINPUT()


####################################################################
####################################################################


# Initialize database connection
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost;" # <-- this might need to change depending on your local dbms name
                      "Database=employee_DB;"
                      "Trusted_Connection=yes;")


#vars
usage = ("Usage: -[emp | dep | adr]\n" 
         "       -emp Fname Lname age salary [manager_id] [dept_id] [addr_id]\n"
         "       -dep name manager_id headqtr_addr_id\n"
         "       -adr street city state\n"
         "Enter 'null' for optional parameters you wish to skip.\n") #usage statement

tableSelect = Table # enumerator for which table has been selected for input

data = [] # list containing lists of data to be inserted into table




#if no parameters passed to program, print usage statement
if len(sys.argv) < 2:
    exit(usage)




# check for input parameters
elif sys.argv[1] == '-emp':
    # user has chosen to input employee data
    tableSelect = Table.EMPLOYEE

elif sys.argv[1] == '-dep':
    #user has chosen to input department data
    tableSelect = Table.DEPARTMENT

elif sys.argv[1] == '-adr':
    #user has chosen to input address data
    tableSelect = Table.ADDRESS

else:
    exit(f"Error: Input parameters not recognized.\n\n{usage}")




#check that the appropriate csv file can be opened/created
#if file doesn't exist and can be created, create it and add header row
try:
    if tableSelect == Table.EMPLOYEE:
        with open('employee.csv', 'at') as filechk:
            if os.stat('employee.csv').st_size == 0:
                csv.writer(filechk).writerow(['employee_id', 'first_name', 'last_name',
                            'age', 'salary', 'manager_id', 'dept_id', 'addr_id'])

    elif tableSelect == Table.DEPARTMENT:
        with open('department.csv', 'at') as filechk: 
            if os.stat('department.csv').st_size == 0:
                csv.writer(filechk).writerow(['dept_id', 'name', 'manager_id', 'headqtr_addr_id'])

    elif tableSelect == Table.ADDRESS:
        with open('address.csv', 'at') as filechk:
            if os.stat('address.csv').st_size == 0:
                csv.writer(filechk).writerow(['addr_id', 'street', 'city', 'state'])

except: exit(f"Error couldn't open {tableSelect.name.tolower()}.csv for inserting.\n"
              "Please verify that you have permission to create/modify this file.")




# if user submitted data through command line parameters, validate it and insert
# into data table if everything correct
if (len(sys.argv) > 2):
    formattedData = validateInput(sys.argv[2:], tableSelect)
    
    #if validateInput() returned an error string, print it and quit program
    if (type(formattedData) == str):
        exit(formattedData + '\n\n' + usage)

    data.append(formattedData)

# if user submitted no data through command line parameters, allow them to
# enter values as coma separated lists
else:
    print("Please enter your data in coma separated lists for insertion ito the "
         f"{tableSelect.name.lower()} table. Enter '\\f' to finish: ")

    userInput = input()
    while userInput != '\\f':
        # separate inputed data into a list
        inputList = split(',', userInput)
        for i in range(len(inputList)): inputList[i] = inputList[i].strip()
        
        # validate inputed data
        formattedData = validateInput(inputList, tableSelect)

        # if validateInput() returned an error string, print it and disregard input
        if (type(formattedData) == str):
            print(formattedData + '\nInput is disregarded.\n')
        else:
            data.append(formattedData)

        userInput = input()




# if user entered data that would be a foreign key, validate that it exists
# in the database
if tableSelect != Table.ADDRESS: #address table has no foreign keys, so skip this if selected table is address
    for i in range(len(data)):
        # establish cursor for queries
        cursor = cnxn.cursor()
        
        # employee table foreign key(s)
        # these are optional, so only check if user gave a value that isn't null
        if tableSelect == Table.EMPLOYEE:
            if len(data[i]) >= 5 and data[i][4] != 'null': # manager_id
                cursor.execute(f"select employee_id from info.employee where employee_id = {data[i][4]}")
                if (len(cursor.fetchall()) == 0):
                    print(f"Error: Value entered for manager_id ({data[i][4]}) for entry '{data[i]}' "
                        "does not match any employee_id in the database. Record will be disregarded.")
                    data.remove(data[i])
                    continue
        
            if len(data[i]) >= 6 and data[i][5] != 'null': # dept_id
                cursor.execute(f"select dept_id from info.department where dept_id = {data[i][5]}")
                if (len(cursor.fetchall()) == 0):
                    print(f"Error: Value entered for dept_id ({data[i][5]}) for entry '{data[i]}' "
                        "does not match any dept_id in the database. Record will be disregarded.")
                    data.remove(data[i])
                    continue

            if len(data[i]) >= 7 and data[i][6] != 'null': # addr_id
                cursor.execute(f"select addr_id from info.address where addr_id = {data[i][6]}")
                if (len(cursor.fetchall()) == 0):
                    print(f"Error: Value entered for addr_id ({data[i][6]}) for entry '{data[i]}' "
                        "does not match any addr_id in the database. Record will be disregarded.")
                    data.remove(data[i])
                    continue
        


        # department table foreign keys
        elif tableSelect == Table.DEPARTMENT:
            #manager_id
            cursor.execute(f"select employee_id from info.employee where employee_id = {data[i][1]}")
            if (len(cursor.fetchall()) == 0):
                print(f"Error: Value entered for manager_id ({data[i][1]}) for entry '{data[i]}' "
                        "does not match any employee_id in the database. Record will be disregarded.")
                data.remove(data[i])
                continue

            #headqtr_addr_id
            cursor.execute(f"select addr_id from info.address where addr_id = {data[i][2]}")
            if (len(cursor.fetchall()) == 0):
                print(f"Error: Value entered for headqtr_addr_id ({data[i][2]}) for entry '{data[i]}' "
                        "does not match any addr_id in the database. Record will be disregarded.")
                data.remove(data[i])
                continue
    ##END FOR
## END IF



# create unique id for new table entry and append nulls for any optional values left out
usedIDs = [] # list of IDs already assigned to other rows with this program
for i in range(len(data)):
    #establish cursor for queries
    cursor = cnxn.cursor()

    # vars
    dbIDs = [] #list of existing IDs in the appropriate database table
    csvIDs = [] #list of existing IDs in the appropriate csv file

    if tableSelect == Table.EMPLOYEE:
        #get IDs from employee table
        cursor.execute("select employee_id from info.employee")
        dbIDs = list(cursor.fetchall()[0])

        #get IDs from employee.csv
        try: csvIDs = list(pd.read_csv('employee.csv')['employee_id'])
        except: pass

        newID = max(dbIDs + csvIDs + usedIDs) + 1
        usedIDs.append(newID)

        # append new ID to front of data list
        data[i] = [newID] + data[i]

        # add nulls to end of list if optional fields are not present
        while len(data[i]) != 8: data[i].append('null')

    elif tableSelect == Table.DEPARTMENT:
        #get IDs from department table
        cursor.execute("select dept_id from info.department")
        dbIDs = list(cursor.fetchall()[0])

        #get IDs from department.csv
        try: csvIDs = list(pd.read_csv('department.csv')['dept_id'])
        except: pass

        newID = max(dbIDs + csvIDs + usedIDs) + 1
        usedIDs.append(newID)

        # append new ID to front of data list
        data[i] = [newID] + data[i]

    elif tableSelect == Table.ADDRESS:
        #get IDs from address table
        cursor.execute("select addr_id from info.address")
        dbIDs = list(cursor.fetchall()[0])

        #get IDs from address.csv
        try: csvIDs = list(pd.read_csv('address.csv')['addr_id'])
        except: pass

        newID = max(dbIDs + csvIDs + usedIDs) + 1
        usedIDs.append(newID)

        # append new ID to front of data list
        data[i] = [newID] + data[i]




print('\n\n')




# write records to appropriate csv file
if (len(data) > 0): # only attempt to write to file if there is data availible to write
    csvFile = tableSelect.name.lower() + '.csv'

    try:
        with open(csvFile, 'at') as csvWrite:
            print('Writing to file...')
            csv.writer(csvWrite).writerows(data)
    except FileNotFoundError: exit(f"Error: couldn't open {csvFile} in current directory. Please check your permissions.")

    print('Write successfull!')