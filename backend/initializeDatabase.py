
import mysql.connector
# from mysql import Error
from config import db_config, sql_script_path, manager_username_trigger_path, student_username_trigger_path,student_fulladdress_trigger_path

def initialize_database():

    print('initializing db...')

    #first make a random connection and create a project database
    #then make a connection with the config (including the name of the database)
    con1 = mysql.connector.connect(
        host='localhost',
        user='root',
        password='seecs@123')
    cur1 = con1.cursor()
    cur1.execute("SHOW DATABASES LIKE project")
    result=cursor.fetchall()

    
    # the following is supposed to run if the project database does NOT exist already
    #it initializes the database with tables, triggers and constraints
    if(len(result)==0):
        cur1.execute("CREATE DATABASE IF NOT EXISTS project")
        con1.commit()
        cur1.execute("USE project")
        #the db is declared now if it didnt exist already 
        #can call the config file with no issues

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
    
        #procedure for running a whole script file------------------------------

        with open(sql_script_path,'r') as sql_file:
            sql_script = sql_file.read()
        
        #splitting the statements in the file 
        sql_statements = sql_script.split(';')
        for statement in sql_statements:
            if statement.strip():  #to insure no blank statements execute
                cursor.execute(statement)
                connection.commit()
        connection.commit()

        #running the trigger queries
        with open(student_username_trigger_path,'r') as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
        
        with open(manager_username_trigger_path,'r') as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)

        with open(student_fulladdress_trigger_path,'r') as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script)
    
        #RUN THESE ONCE !!!
        #adding in a default student and admin:
        query = "INSERT INTO Student(cms,sFirstName,sLastName,sAge,sEmail,sPhoneNumber,city,street,house_no,roomNumber,sBatch,sPassword) VALUES (429551,'Maheen','Ahmed',19,'maheenahmed@gmail.com',03049991681,'Karachi','abc','xyz',316,2022,'seecs@123')"
        cursor.execute(query)
        connection.commit()
        query = "INSERT INTO Manager(MID,mFirstName,mLastName,mPassword) VALUES (1234,'John','Doe','seecs@123')"
        cursor.execute(query)
        connection.commit()
        query = "INSERT INTO Student(cms,sFirstName,sLastName,sAge,sEmail,sPhoneNumber,city,street,house_no,roomNumber,sBatch,sPassword) VALUES (423482,'Muzaynah','Farrukh',19,'muzaynahfarrukh@gmail.com',123,'Karachi','abc','xyz',316,2022,'seecs@123')"
        cursor.execute(query)
        connection.commit()

    cursor.close()
    connection.close()