#for testing

from config import procedures_path,db_config,grant_student_path,db_config_student
import mysql.connector

con = mysql.connector.connect(**db_config_student)
cursor=con.cursor()

# with open(procedures_path,'r') as sql_file:
#         sql_script = sql_file.read()
        
#         # #splitting the statements in the file 
#         # sql_statements = sql_script.split('DELIMITER;')
#         # print(sql_statements)
# cursor.execute(sql_script)

# with open(grant_student_path,'r') as sql_file:
#             sql_script = sql_file.read()
# cursor.execute(sql_script)
# out_params = [None] * 18 
# # cursor.callproc('get_all_student_data', [429551] + out_params)
# firstName, lastName, age, email, phoneNumber, city, street, house_no, full_address, roomNumber, batch, username, password, program, hostel_id, department_id, hostel_name, department_name=None
# cursor.callproc('get_all_student_data', [429551,firstName, lastName, age, email, phoneNumber, city, street, house_no, full_address, roomNumber, batch, username, password, program, hostel_id, department_id, hostel_name, department_name])
# # print(out_params)
# # Retrieve the values from the out_params list
# # firstName, lastName, age, email, phoneNumber, city, street, house_no, full_address, roomNumber, batch, username, password, program, hostel_id, department_id, hostel_name, department_name = out_params

# print(firstName)

# Assuming 18 OUT parameters based on your stored procedure
out_params = [None] * 18
args1=[429551]+out_params
print(args1)
# Call the stored procedure
result=cursor.callproc('get_all_student_data', args=args1)
print(result)
# Retrieve the values from the out_params list
# firstName, lastName, age, email, phoneNumber, city, street, house_no, full_address, roomNumber, batch, username, password, program, hostel_id, department_id, hostel_name, department_name = out_params
print(args1)
# Print or use the retrieved values as needed
# print(firstName)
