
import mysql.connector
# from mysql import Error
from config import db_config, sql_script_path, manager_username_trigger_path, student_username_trigger_path,student_fulladdress_trigger_path,procedures_path,grant_student_path

def initialize_database():

    #first make a random connection and create a project database
    #then make a connection with the config (including the name of the database)
    con1 = mysql.connector.connect(
        host='localhost',
        user='root',
        password='seecs@123')
    cur1 = con1.cursor()
    cur1.execute("SHOW DATABASES LIKE 'project'")
    result=cur1.fetchall()

    # the following is supposed to run if the project database does NOT exist already
    #it initializes the database with tables, triggers, constraints, and some default data
    if(len(result)==0):
        print('initializing db...')
        cur1.execute("CREATE DATABASE IF NOT EXISTS project")
        con1.commit()
        cur1.execute("USE project")
        #the db is declared now if it didnt exist already 
        #can call the config file with no issues

        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()
    
        #initializing all tables-----------------------------------------

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
        connection.commit() 
        cursor.nextset()
    
        #running all procedures stored in one file------------------------------
        with open(procedures_path,'r') as sql_file:
            sql_script = sql_file.read()
        
        #splitting the statements in the file 
        sql_statements = sql_script.split('--')
        # print(sql_statements)
        for statement in sql_statements:
            if statement.strip():  #to insure no blank statements execute
                cursor.execute(statement)
                # connection.commit()
        # cursor.execute(sql_script)
        connection.commit()
        cursor.nextset()



        #initializing department and hostel
        query = '''
                    insert into department(did,dname) values
                    (1,'SEECS'),
                    (2,'NBS'),
                    (3,'NICE'),
                    (4,'S3H'),
                    (5,'ASAB'),
                    (6,'SCEE'),
                    (7,'SMME'),
                    (8,'SNS'),
                    (9,'SCME'),
                    (10,'SINES'),
                    (11,'SADA'),
                    (12,'RIMMS')
                    ;
                '''
        cursor.execute(query)
        connection.commit()
        query = '''
                    insert into hostel(hid,hName) values 
                        (1,'Zainab'),
                        (2,'Ayesha'),
                        (3,'Khadija'),
                        (4,'Amna')
                    ;
                '''
        cursor.execute(query)
        connection.commit()

        #initializing some managers
        query = '''
                    insert into manager(mid,mFirstname, mLastName,mPassword,mEmail,HID) values
	                    (1,'Samina','Baji','seecs@123','maheenahmed2004@outlook.com',4),
                        (2,'Aqsa','Qazi','seecs@123','maheenahmed2004@outlook.com',1)
                    ;
                '''
        cursor.execute(query)
        connection.commit()


        #initializing users
        query ="create USER IF NOT EXISTS 'student'@'localhost' IDENTIFIED BY 'seecs@123';"
        cursor.execute(query)
        connection.commit()
        query = "create USER IF NOT EXISTS 'manager'@'localhost' IDENTIFIED BY 'seecs@123'"
        cursor.execute(query)
        connection.commit()
        cursor.nextset()


        #granting users priviliges --------------------------------------------------------------------
        with open(grant_student_path,'r') as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script, multi=True)

        # print(sql_script)
        
        #adding in default students and admin:
        
        #reinitializing the cursor
        cursor.close()
        connection.close()

        connection=mysql.connector.connect(**db_config)
        cursor=connection.cursor()

        query = "INSERT INTO Student(cms,sFirstName,sLastName,sAge,sEmail,sPhoneNumber,city,street,house_no,sRoomNumber,sBatch,sPassword,did,hid) VALUES (429551,'Maheen','Ahmed',19,'maheenahmed2004@outlook.com',03049991681,'Karachi','abc','xyz',316,2022,'seecs@123',1,1)"
        cursor.execute(query)
        connection.commit()
        query = "INSERT INTO Manager(MID,mFirstName,mLastName,mPassword,mEmail,HID) VALUES (1234,'John','Doe','seecs@123','muzaynah19@gmail.com',3)"
        cursor.execute(query)
        connection.commit()
        query = "INSERT INTO Student(cms,sFirstName,sLastName,sAge,sEmail,sPhoneNumber,city,street,house_no,sRoomNumber,sBatch,sPassword,did,hid) VALUES (423482,'Muzaynah','Farrukh',19,'muzaynah19@gmail.com',123,'Karachi','abc','xyz',316,2022,'seecs@123',1,4)"
        cursor.execute(query)
        connection.commit()

        query = "INSERT INTO Student(cms,sFirstName,sLastName,sAge,sEmail,sPhoneNumber,city,street,house_no,sRoomNumber,sBatch,sPassword,did,hid) VALUES (404520,'Isra','Mansoor',19,'isramansoor@gmail.com',123,'Islamabad','abc','xyz',428,2022,'seecs@123',1,2)"
        cursor.execute(query)
        connection.commit()

        query = '''INSERT INTO attendanceevent values
	('2004-10-12',"Present",429551),
    ('2004-10-13',"Absent",429551),
    ('2004-10-12',"Present",404520),
    ('2004-10-12',"Absent",423482);'''
        cursor.execute(query)
        connection.commit()
        
        cursor.close()
        connection.close()
    else:
        print('using existing db')
    cur1.close()
    con1.close()