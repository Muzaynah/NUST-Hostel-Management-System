#for testing

from config import procedures_path,db_config,grant_student_path,db_config_student,db_config_manager
import mysql.connector

con = mysql.connector.connect(**db_config_manager)
cursor=con.cursor()

# # student_data = {label: entry.get() for label, entry in self.entry_fields.items()}
# print("Switching to student Section\nAdding student:")
# # print(student_data)
# # Get department ID from dname
# departmentname = 'SEECS'
# cursor.execute(f"SELECT dID FROM Department WHERE dname = '"+departmentname+"';")
# department_id = cursor.fetchone()  # Fetch the first column value
# print(department_id[0])

# # Adding into the student table
# query = '''
#         INSERT INTO Student(cms, sFirstName, sLastName, sAge, sEmail, sPhoneNumber, city, street, house_no, sRoomNumber,
#                         sBatch, sPassword, sProgram, HID, dID) 
#         VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
# '''

# student_values = (429552, 'Maheen', 'Ahmed', 19, 'maheenahmed2004@outlook.com', 3049991681, 'abu dhabi','street', 1308, 316, 2022, 'seecs@123', None, 1, 1)
# print(len(student_values))

# try:
#         cursor.execute(query, student_values)
#         print(cursor.fetchall())
#         con.commit()
#         print("Student added successfully!")
#         # Call the callback function to update the treeview in the AdminStudent class

# except mysql.connector.Error as err:
#         print(f"Error: {err}")

cursor.execute("select * from student;")
result=cursor.fetchall()
print(result)
