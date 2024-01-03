
import mysql.connector
# from mysql import Error
from config import db_config, sql_script_path, manager_username_trigger_path, student_username_trigger_path,student_fulladdress_trigger_path,procedures_path,grants_path,views_path,encryption_path

def initialize_database():

    #first make a random connection and create a project database
    #then make a connection with the config (including the name of the database)
    con1 = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Mf19*twdc')
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

        # #encryption procedures
        # with open(encryption_path,'r') as sql_file:
        #     sql_script = sql_file.read()
        # sql_statements = sql_script.split('--')
        # for statement in sql_statements:
        #     if statement.strip():  #to insure no blank statements execute
        #         cursor.execute(statement)
        #         connection.commit()
        
        # cursor.nextset()

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
                    VALUES (429551,'Maheen','Ahmed',19,'maheenahmed2004@outlook.com','03049991681','Karachi','abc','xyz',316,2022,'seecs@123',1,1),
                    (423482,'Muzaynah','Farrukh',19,'muzaynah19@gmail.com','03112119384','Karachi','abc','xyz',316,2022,'seecs@123',1,4),
                    (404520,'Isra','Mansoor',19,'isramansoor@gmail.com','03235050952','Islamabad','abc','xyz',428,2022,'seecs@123',1,2),
                    (436789, 'Ayesha', 'Akhtar', 19, 'ayesha.akhtar@gmail.com', '03678901234', 'Karachi', 'Nazimabad', 'LMN Street', 212, 2022, 'seecs@123', 2, 1),
                    (445678, 'Sara', 'Khan', 20, 'sara.khan@gmail.com', '03789012345', 'Lahore', 'Defence', 'JKL Road', 114, 2022, 'seecs@123', 3, 2),
                    (111111, 'Ayesha', 'Ali', 19, 'ayesha.ali@example.com', '03011111111', 'Karachi', 'Street1', 'House1', 101, 2022, 'seecs@123', 1, 1),
                    (111112, 'Hina', 'Khan', 20, 'hina.khan@example.com', '03011111112', 'Lahore', 'Street1', 'House2', 102, 2022, 'seecs@123', 1, 1),
                    (111113, 'Nida', 'Ahmed', 18, 'nida.ahmed@example.com', '03011111113', 'Islamabad', 'Street1', 'House3', 103, 2022, 'seecs@123', 1, 1),
                    (111114, 'Saima', 'Malik', 19, 'saima.malik@example.com', '03011111114', 'Karachi', 'Street1', 'House4', 104, 2022, 'seecs@123', 1, 1),
                    (111115, 'Farah', 'Saeed', 20, 'farah.saeed@example.com', '03011111115', 'Lahore', 'Street1', 'House5', 105, 2022, 'seecs@123', 1, 1),
                    (111116, 'Zainab', 'Rashid', 18, 'zainab.rashid@example.com', '03011111116', 'Islamabad', 'Street1', 'House6', 106, 2022, 'seecs@123', 1, 1),
                    (111117, 'Mariam', 'Nawaz', 19, 'mariam.nawaz@example.com', '03011111117', 'Karachi', 'Street1', 'House7', 107, 2022, 'seecs@123', 1, 1),
                    (111118, 'Aisha', 'Siddiq', 20, 'aisha.siddiq@example.com', '03011111118', 'Lahore', 'Street1', 'House8', 108, 2022, 'seecs@123', 1, 1),

                    (222221, 'Saba', 'Ahmed', 19, 'saba.ahmed@example.com', '03022222221', 'Islamabad', 'Street2', 'House1', 201, 2022, 'seecs@123', 1, 2),
                    (222222, 'Tania', 'Khan', 20, 'tania.khan@example.com', '03022222222', 'Karachi', 'Street2', 'House2', 202, 2022, 'seecs@123', 1, 2),
                    (222223, 'Sadia', 'Rasheed', 18, 'sadia.rasheed@example.com', '03022222223', 'Lahore', 'Street2', 'House3', 203, 2022, 'seecs@123', 1, 2),
                    (222224, 'Amina', 'Akhtar', 19, 'amina.akhtar@example.com', '03022222224', 'Islamabad', 'Street2', 'House4', 204, 2022, 'seecs@123', 1, 2),
                    (222225, 'Neha', 'Raza', 20, 'neha.raza@example.com', '03022222225', 'Karachi', 'Street2', 'House5', 205, 2022, 'seecs@123', 1, 2),
                    (222226, 'Sara', 'Qureshi', 18, 'sara.qureshi@example.com', '03022222226', 'Lahore', 'Street2', 'House6', 206, 2022, 'seecs@123', 1, 2),
                    (222227, 'Bushra', 'Malik', 19, 'bushra.malik@example.com', '03022222227', 'Islamabad', 'Street2', 'House7', 207, 2022, 'seecs@123', 1, 2),
                    (222228, 'Sadia', 'Saeed', 20, 'sadia.saeed@example.com', '03022222228', 'Karachi', 'Street2', 'House8', 208, 2022, 'seecs@123', 1, 2),

                    (333331, 'Sara', 'Aslam', 19, 'sara.aslam@example.com', '03033333331', 'Islamabad', 'Street3', 'House1', 301, 2022, 'seecs@123', 1, 3),
                    (333332, 'Zara', 'Iqbal', 20, 'zara.iqbal@example.com', '03033333332', 'Karachi', 'Street3', 'House2', 302, 2022, 'seecs@123', 1, 3),
                    (333333, 'Madiha', 'Hassan', 18, 'madiha.hassan@example.com', '03033333333', 'Lahore', 'Street3', 'House3', 303, 2022, 'seecs@123', 1, 3),
                    (333334, 'Amina', 'Qureshi', 19, 'amina.qureshi@example.com', '03033333334', 'Islamabad', 'Street3', 'House4', 304, 2022, 'seecs@123', 1, 3),
                    (333335, 'Tahira', 'Ahmed', 20, 'tahira.ahmed@example.com', '03033333335', 'Karachi', 'Street3', 'House5', 305, 2022, 'seecs@123', 1, 3),
                    (333336, 'Fauzia', 'Saeed', 18, 'fauzia.saeed@example.com', '03033333336', 'Lahore', 'Street3', 'House6', 306, 2022, 'seecs@123', 1, 3),
                    (333337, 'Nadia', 'Rehman', 19, 'nadia.rehman@example.com', '03033333337', 'Islamabad', 'Street3', 'House7', 307, 2022, 'seecs@123', 1, 3),
                    (333338, 'Hira', 'Raza', 20, 'hira.raza@example.com', '03033333338', 'Karachi', 'Street3', 'House8', 308, 2022, 'seecs@123', 1, 3),

                    (444441, 'Samina', 'Yousaf', 19, 'samina.yousaf@example.com', '03044444441', 'Lahore', 'Street4', 'House1', 401, 2022, 'seecs@123', 1, 4),
                    (444442, 'Naima', 'Khalid', 20, 'naima.khalid@example.com', '03044444442', 'Islamabad', 'Street4', 'House2', 402, 2022, 'seecs@123', 1, 4),
                    (444443, 'Ayesha', 'Akram', 18, 'ayesha.akram@example.com', '03044444443', 'Karachi', 'Street4', 'House3', 403, 2022, 'seecs@123', 1, 4),
                    (444444, 'Sadia', 'Nawaz', 19, 'sadia.nawaz@example.com', '03044444444', 'Lahore', 'Street4', 'House4', 404, 2022, 'seecs@123', 1, 4),
                    (444445, 'Fariha', 'Malik', 20, 'fariha.malik@example.com', '03044444445', 'Islamabad', 'Street4', 'House5', 405, 2022, 'seecs@123', 1, 4),
                    (444446, 'Irum', 'Ali', 18, 'irum.ali@example.com', '03044444446', 'Karachi', 'Street4', 'House6', 406, 2022, 'seecs@123', 1, 4),
                    (444447, 'Saima', 'Rashid', 19, 'saima.rashid@example.com', '03044444447', 'Lahore', 'Street4', 'House7', 407, 2022, 'seecs@123', 1, 4),
                    (444448, 'Nazia', 'Siddiq', 20, 'nazia.siddiq@example.com', '03044444448', 'Islamabad', 'Street4', 'House8', 408, 2022, 'seecs@123', 1, 4);

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

        query_statements = query.split(';')
        for query_statement in query_statements:
            if query_statement.strip():  #to insure no blank statements execute
                cursor.execute(query_statement)
                connection.commit()
        connection.commit()
        # cursor.execute(query,multi=True)
        # connection.commit()

        #reinitializing to reset
        cursor.close()
        connection.close()

        connection=mysql.connector.connect(**db_config)
        cursor=connection.cursor()

        con2=mysql.connector.connect(**db_config)
        cur2=con2.cursor()

        query = '''
                    INSERT INTO Guardian (gName, gPhoneNumber, gEmail, cms)
                    VALUES 
                    ('Saima Ahmed',   03004999222, 'saima.ahmed@gmail.com', 429551),
                    ('Farrukh Zafar', 03211234444, 'farrukh.zafar@gmail.com', 423482),
                    ('Mansoor Ali',   03451235555, 'mansoor.ali@gmail.com', 404520),
                    ('Akhtar Khan',   03678901111, 'akhtar.khan@gmail.com', 436789),
                    ('Kashan Khan',   03789012222, 'kashan.khan@gmail.com', 445678),
                    
                    -- Guardians for Hostel ID 1 students
                    ('Ali Ahmed', '03011111119', 'ali.ahmed@example.com', 111111),
                    ('Hina Khan', '03011111120', 'hina.khan@example.com', 111111),
                    ('Nida Ahmed', '03011111121', 'nida.ahmed@example.com', 111111),

                    ('Rashid Malik', '03011111122', 'rashid.malik@example.com', 111114),
                    ('Saeed Farah', '03011111123', 'saeed.farah@example.com', 111115),
                    ('Rasheed Zainab', '03011111124', 'rasheed.zainab@example.com', 111116),

                    ('Nawaz Mariam', '03011111125', 'nawaz.mariam@example.com', 111117),
                    ('Aisha Siddiq', '03011111126', 'aisha.siddiq@example.com', 111118),
                    ('Siddiq Amina', '03011111127', 'siddiq.amina@example.com', 111118),

                    -- Guardians for Hostel ID 2 students
                    ('Ahmed Saba', '03022222229', 'ahmed.saba@example.com', 222221),
                    ('Khan Tania', '03022222230', 'khan.tania@example.com', 222222),
                    ('Rasheed Sadia', '03022222231', 'rasheed.sadia@example.com', 222223),

                    ('Akhtar Amina', '03022222232', 'akhtar.amina@example.com', 222224),
                    ('Raza Neha', '03022222233', 'raza.neha@example.com', 222225),
                    ('Qureshi Sara', '03022222234', 'qureshi.sara@example.com', 222226),

                    ('Malik Bushra', '03022222235', 'malik.bushra@example.com', 222227),
                    ('Saeed Sadia', '03022222236', 'saeed.sadia@example.com', 222228),
                    ('Siddiq Aisha', '03022222237', 'siddiq.aisha@example.com', 222228),

                    -- Guardians for Hostel ID 3 students
                    ('Khan Mariam', '03033333339', 'khan.mariam@example.com', 333331),
                    ('Ahmed Aisha', '03033333340', 'ahmed.aisha@example.com', 333332),
                    ('Raza Bushra', '03033333341', 'raza.bushra@example.com', 333333),

                    ('Saeed Hina', '03033333342', 'saeed.hina@example.com', 333334),
                    ('Rasheed Sadia', '03033333343', 'rasheed.sadia@example.com', 333335),
                    ('Qureshi Saba', '03033333344', 'qureshi.saba@example.com', 333336),

                    ('Ali Neha', '03033333345', 'ali.neha@example.com', 333337),
                    ('Tania Zainab', '03033333346', 'tania.zainab@example.com', 333338),
                    ('Malik Sara', '03033333347', 'malik.sara@example.com', 333338),

                    -- Guardians for Hostel ID 4 students
                    ('Khan Fatima', '03044444449', 'khan.fatima@example.com', 444441),
                    ('Ahmed Nida', '03044444450', 'ahmed.nida@example.com', 444442),
                    ('Raza Zainab', '03044444451', 'raza.zainab@example.com', 444443),

                    ('Saeed Saba', '03044444452', 'saeed.saba@example.com', 444444),
                    ('Rasheed Hina', '03044444453', 'rasheed.hina@example.com', 444445),
                    ('Qureshi Mariam', '03044444454', 'qureshi.mariam@example.com', 444446),

                    ('Ali Neha', '03044444455', 'ali.neha@example.com', 444447),
                    ('Tania Sara', '03044444456', 'tania.sara@example.com', 444448),
                    ('Malik Aisha', '03044444457', 'malik.aisha@example.com', 444448);
                '''
        
        # cur2.execute(query,multi=True)
        # con2.commit()
        query_statements = query.split(';')
        for query_statement in query_statements:
            if query_statement.strip():  #to insure no blank statements execute
                cur2.execute(query_statement)
                con2.commit()
        con2.commit()


        query = '''
            INSERT INTO attendanceevent (ADate, Attendance, cms)
            VALUES
            ('2023-01-02', 'Present', 429551),
            ('2023-01-02', 'Absent', 423482),
            ('2023-01-02', 'Present', 404520),
            ('2023-01-02', 'Absent', 436789),

            ('2023-12-31', 'Present', 429551),
            ('2023-12-31', 'Absent', 423482),
            ('2023-12-31', 'Leave', 404520),
            ('2023-12-31', 'Present', 436789),
            ('2023-12-31', 'Absent', 445678),

            ('2023-12-31', 'Present', 111111),
            ('2023-12-31', 'Absent', 111112),
            ('2023-12-31', 'Leave', 111113),
            ('2023-12-31', 'Present', 111114),
            ('2023-12-31', 'Absent', 111115),
            
            ('2023-12-31', 'Present', 111116),
            ('2023-12-31', 'Absent', 111117),
            ('2023-12-31', 'Leave', 111118),
            ('2023-12-31', 'Present', 222221),
            ('2023-12-31', 'Absent', 222222),

            ('2023-12-31', 'Present', 222223),
            ('2023-12-31', 'Absent', 222224),
            ('2023-12-31', 'Leave', 222225),
            ('2023-12-31', 'Present', 222226),
            ('2023-12-31', 'Absent', 222227),
            
            ('2023-12-31', 'Present', 222228),
            ('2023-12-31', 'Absent', 333331),
            ('2023-12-31', 'Leave', 333332),
            ('2023-12-31', 'Present', 333333),
            ('2023-12-31', 'Absent', 333334),

            ('2023-12-31', 'Present', 333335),
            ('2023-12-31', 'Absent', 333336),
            ('2023-12-31', 'Leave', 333337),
            ('2023-12-31', 'Present', 333338),
            ('2023-12-31', 'Absent', 444441),

            ('2023-12-31', 'Present', 444442),
            ('2023-12-31', 'Absent', 444443),
            ('2023-12-31', 'Leave', 444444),
            ('2023-12-31', 'Present', 444445),
            ('2023-12-31', 'Absent', 444446),

            ('2023-12-31', 'Present', 444447),
            ('2023-12-31', 'Absent', 444448),
            
            ('2024-01-02', 'Present', 111111),
            ('2024-01-02', 'Absent', 111112),
            ('2024-01-02', 'Leave', 111113),
            ('2024-01-02', 'Present', 111114),
            ('2024-01-02', 'Absent', 111115),
            
            ('2024-01-02', 'Present', 111116),
            ('2024-01-02', 'Absent', 111117),
            ('2024-01-02', 'Leave', 111118),
            ('2024-01-02', 'Present', 222221),
            ('2024-01-02', 'Absent', 222222),

            ('2024-01-02', 'Present', 222223),
            ('2024-01-02', 'Absent', 222224),
            ('2024-01-02', 'Leave', 222225),
            ('2024-01-02', 'Present', 222226),
            ('2024-01-02', 'Absent', 222227),
            
            ('2024-01-02', 'Present', 222228),
            ('2024-01-02', 'Absent', 333331),
            ('2024-01-02', 'Leave', 333332),
            ('2024-01-02', 'Present', 333333),
            ('2024-01-02', 'Absent', 333334),

            ('2024-01-02', 'Present', 333335),
            ('2024-01-02', 'Absent', 333336),
            ('2024-01-02', 'Leave', 333337),
            ('2024-01-02', 'Present', 333338),
            ('2024-01-02', 'Absent', 444441),

            ('2024-01-02', 'Present', 444442),
            ('2024-01-02', 'Absent', 444443),
            ('2024-01-02', 'Leave', 444444),
            ('2024-01-02', 'Present', 444445),
            ('2024-01-02', 'Absent', 444446),

            ('2024-01-02', 'Present', 444447),
            ('2024-01-02', 'Absent', 444448),

            ('2024-01-01', 'Present', 429551),
            ('2024-01-01', 'Absent', 423482),
            ('2024-01-01', 'Leave', 404520),
            ('2024-01-01', 'Present', 436789),
            ('2024-01-01', 'Absent', 445678),

            ('2024-01-01', 'Present', 111111),
            ('2024-01-01', 'Absent', 111112),
            ('2024-01-01', 'Leave', 111113),
            ('2024-01-01', 'Present', 111114),
            ('2024-01-01', 'Absent', 111115),

            ('2024-01-01', 'Present', 111116),
            ('2024-01-01', 'Absent', 111117),
            ('2024-01-01', 'Leave', 111118),
            ('2024-01-01', 'Present', 222221),
            ('2024-01-01', 'Absent', 222222),

            ('2024-01-01', 'Present', 222223),
            ('2024-01-01', 'Absent', 222224),
            ('2024-01-01', 'Leave', 222225),
            ('2024-01-01', 'Present', 222226),
            ('2024-01-01', 'Absent', 222227),

            ('2024-01-01', 'Present', 222228),
            ('2024-01-01', 'Absent', 333331),
            ('2024-01-01', 'Leave', 333332),
            ('2024-01-01', 'Present', 333333),
            ('2024-01-01', 'Absent', 333334),

            ('2024-01-01', 'Present', 333335),
            ('2024-01-01', 'Absent', 333336),
            ('2024-01-01', 'Leave', 333337),
            ('2024-01-01', 'Present', 333338),
            ('2024-01-01', 'Absent', 444441),

            ('2024-01-01', 'Present', 444442),
            ('2024-01-01', 'Absent', 444443),
            ('2024-01-01', 'Leave', 444444),
            ('2024-01-01', 'Present', 444445),
            ('2024-01-01', 'Absent', 444446),

            ('2024-01-01', 'Present', 444447),
            ('2024-01-01', 'Absent', 444448);

        '''
        cur2.execute(query,multi=True)
        con2.commit()

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