import os
# configs that can be altered


current_user_id = -1
current_user_type = ""

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ISR@m@nsoor0785',
    'database': 'project'
}

db_config_student ={
    'host':'localhost',
    'user':'student',
    'password':'seecs@123',
    'database':'project'
}

db_config_manager ={
    'host':'localhost',
    'user':'manager',
    'password':'seecs@123',
    'database':'project'
}

current_script_path = os.path.abspath(__file__)
db_folder_path = os.path.dirname(os.path.dirname(current_script_path))
nhms_folder_path = os.path.join(db_folder_path,'NUST-Hostel-Management-System')
sqlscripts_folder_path = os.path.join(nhms_folder_path, 'sql-scripts')

sql_script_path = os.path.join(sqlscripts_folder_path,'tables.sql')

procedures_path = os.path.join(sqlscripts_folder_path,'procedures.sql')
grant_student_path = os.path.join(sqlscripts_folder_path,'grant_student.sql')

student_username_trigger_path = os.path.join(sqlscripts_folder_path,'student_username_trigger.sql')
manager_username_trigger_path = os.path.join(sqlscripts_folder_path,'manager_username_trigger.sql')
student_fulladdress_trigger_path = os.path.join(sqlscripts_folder_path,'student_fulladdress_trigger.sql')

# change to your paths
# sql_script_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\tables.sql'
# student_username_trigger_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\student_username_trigger.sql'
# manager_username_trigger_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\manager_username_trigger.sql'
# student_fulladdress_trigger_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\student_fulladdress_trigger.sql'