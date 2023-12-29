import os
# configs that can be altered


current_user_id = -1

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'seecs@123',
    'database': 'project'
}

current_script_path = os.path.abspath(__file__)
db_folder_path = os.path.dirname(os.path.dirname(current_script_path))
nhms_folder_path = os.path.join(db_folder_path,'NUST-Hostel-Management-System')
sqlscripts_folder_path = os.path.join(nhms_folder_path, 'sql-scripts')
sql_script_path = os.path.join(sqlscripts_folder_path,'tables.sql')

student_username_trigger_path = os.path.join(sqlscripts_folder_path,'student_username_trigger.sql')
manager_username_trigger_path = os.path.join(sqlscripts_folder_path,'manager_username_trigger.sql')
student_fulladdress_trigger_path = os.path.join(sqlscripts_folder_path,'student_fulladdress_trigger.sql')
# change to your paths
# sql_script_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\tables.sql'
# student_username_trigger_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\student_username_trigger.sql'
# manager_username_trigger_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\manager_username_trigger.sql'
# student_fulladdress_trigger_path = r'C:\Users\PC\Desktop\db\NUST-Hostel-Management-System\sql-scripts\student_fulladdress_trigger.sql'