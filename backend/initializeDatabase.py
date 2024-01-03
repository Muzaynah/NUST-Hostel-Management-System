
import mysql.connector
# from mysql import Error
from config import db_config, sql_script_path, manager_username_trigger_path, student_username_trigger_path,student_fulladdress_trigger_path,procedures_path,grants_path,views_path

def initialize_database():

    #first make a random connection and create a project database
    #then make a connection with the config (including the name of the database)
    con1 = mysql.connector.connect(
        host='localhost',
        user='root',
        password='')
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


        #initializing users
        query ="create USER IF NOT EXISTS 'student'@'localhost' IDENTIFIED BY 'seecs@123';"
        cursor.execute(query)
        connection.commit()
        query = "create USER IF NOT EXISTS 'manager'@'localhost' IDENTIFIED BY 'seecs@123'"
        cursor.execute(query)
        connection.commit()
        cursor.nextset()

        #creating views
        with open(views_path,'r') as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script,multi=True)

        #reinitializing to reset
        cursor.close()
        connection.close()

        connection=mysql.connector.connect(**db_config)
        cursor=connection.cursor()

        #granting users priviliges --------------------------------------------------------------------
        with open(grants_path,'r') as sql_file:
            sql_script = sql_file.read()
        cursor.execute(sql_script, multi=True)

        # print(sql_script)
        
        #adding in default students and admin:
        
        #reinitializing the cursor
        cursor.close()
        connection.close()

        connection=mysql.connector.connect(**db_config)
        cursor=connection.cursor()

        query = '''
                    INSERT INTO Student(cms,sFirstName,sLastName,sAge,sEmail,sPhoneNumber,city,street,house_no,sRoomNumber,sBatch,sPassword,did,hid)
                    VALUES (429551,'Maheen','Ahmed',19,'maheenahmed2004@outlook.com',03049991681,'Karachi','abc','xyz',316,2022,'seecs@123',1,1),
                    (423482,'Muzaynah','Farrukh',19,'muzaynah19@gmail.com',123,'Karachi','abc','xyz',316,2022,'seecs@123',1,4),
                    (404520,'Isra','Mansoor',19,'isramansoor@gmail.com',123,'Islamabad','abc','xyz',428,2022,'seecs@123',1,2),
                    (436789, 'Ayesha', 'Akhtar', 19, 'ayesha.akhtar@gmail.com', 03678901234, 'Karachi', 'Nazimabad', 'LMN Street', 212, 2022, 'seecs@123', 2, 1),
                    (445678, 'Sara', 'Khan', 20, 'sara.khan@gmail.com', 03789012345, 'Lahore', 'Defence', 'JKL Road', 114, 2022, 'seecs@123', 3, 2);
                '''
        cursor.execute(query)
        connection.commit()

        #initializing some managers
        query = '''
                    insert into manager(mid,mFirstname, mLastName,mPassword,mEmail,HID) values
	                    (1236,'Samina','Baji','seecs@123','maheenahmed2004@outlook.com',4),
                        (6712,'Aqsa','Qazi','seecs@123','maheenahmed2004@outlook.com',1),
                        (1234, 'John', 'Doe', 'seecs@123', 'muzaynah19@gmail.com', 3),
                        (4111, 'Bilal', 'Raza', 'seecs@123', 'bilal.raza@email.com', 2),
                        (5098, 'Sana', 'Ahmed', 'seecs@123', 'sana.ahmed@email.com', 1);
                    '''

        cursor.execute(query)
        connection.commit()


        query = '''
                    INSERT INTO Guardian (gName, gPhoneNumber, gEmail, cms)
                    VALUES 
                    ('Saima Ahmed',   30049992222, 'saima.ahmed@gmail.com', 429551),
                    ('Farrukh Zafar', 32112344444, 'farrukh.zafar@gmail.com', 423482),
                    ('Mansoor Ali',   34512355555, 'mansoor.ali@gmail.com', 404520),
                    ('Akhtar Khan',   36789011111, 'akhtar.khan@gmail.com', 436789),
                    ('Kashan Khan',   37890122222, 'kashan.khan@gmail.com', 445678);
     
                '''
        cursor.execute(query)
        connection.commit()
       


        query = '''
            INSERT INTO attendanceevent (AEDate, AEStatus, cms)
            VALUES
            ('2023-01-01', 'Present', 429551),
            ('2023-01-01', 'Present', 429551),
            ('2023-01-02', 'Absent', 423482),
            ('2023-01-03', 'Present', 404520),
            ('2023-01-04', 'Absent', 436789);
        '''

        query = '''
                    INSERT INTO Complaint (CDescription, CStatus, CDate, cms)
                    VALUES 
                    ('Broken chair in my room.', 'Pending', '2023-01-01', 429551),
                    ('AC not working in common area.', 'Resolved', '2023-01-02', 423482),
                    ('Wi-Fi connectivity issues.', 'Pending', '2023-01-03', 404520),
                    ('Leakage in the ceiling.', 'Resolved', '2023-01-04', 436789),
                    ('Dirty bathrooms on the floor.', 'Pending', '2023-01-05', 445678);
                '''
        cursor.execute(query)
        connection.commit()


        query = '''
                    INSERT INTO Outpass (LeavingDate, JoiningDate, Purpose, OStatus, cms)
                    VALUES 
                    ('2023-02-01', '2023-02-03', 'Family Function', 'Pending', 429551),
                    ('2023-02-05', '2023-02-07', 'Medical Emergency', 'Approved', 423482),
                    ('2023-02-10', '2023-02-12', 'Vacation', 'Pending', 404520),
                    ('2023-02-15', '2023-02-17', 'Personal Reasons', 'Approved', 436789),
                    ('2023-02-20', '2023-02-22', 'Visit Home', 'Pending', 445678);
                
                '''
        cursor.execute(query)
        connection.commit()

        query = '''
                    INSERT INTO Notifications (NText, NDate, HID)
                    VALUES
                    ('Hostel Meeting on 2023-02-10', '2023-02-08', 1),
                    ('Maintenance Notice - Water Supply on 2023-02-15', '2023-02-12', 2),
                    ('Upcoming Cultural Event on 2023-02-20', '2023-02-18', 3),
                    ('Room Inspection on 2023-02-25', '2023-02-23', 4),
                    ('Important Announcement - Exams Schedule on 2023-03-01', '2023-02-27', 1);

                '''
        cursor.execute(query)
        connection.commit()
        
        cursor.close()
        connection.close()
    else:
        print('using existing db')
    cur1.close()
    con1.close()