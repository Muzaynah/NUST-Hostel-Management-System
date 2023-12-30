import tkinter as tk
from tkinter import Label, Button, PhotoImage, ttk, Entry, Toplevel
import mysql.connector
from config import db_config_manager
import config

class AdminStudent(tk.Frame):
    def __init__(self, master, show_add_student):
        super().__init__(master, bg='white')
        self.master = master
        self.show_add_student = show_add_student
        self.connection=mysql.connector.connect(**db_config_manager)
        self.cursor=self.connection.cursor()
        self.hostel_id=-1
        self.create_widgets()

    def create_widgets(self):

        # Create a frame to center the treeview
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        # Create a treeview for displaying students
        columns = ('CMS', 'First Name', 'Last Name', 'Age', 'Email', 'Phone Number', 'City', 'Street', 'House Number', 'Room Number','Batch','Department ID', 'Department Name', 'Program','Hostel ID','Hostel Name')
        self.student_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        #getting initial data for treeview-----------------------------------

        #getting hostel id of the logged in manager
        query =f"select hid from manager where mid={config.current_user_id[0]}"
        self.cursor.execute(query)
        self.hostel_id=self.cursor.fetchone()
        # -------------------------------------------------------------
        # #fetching student data for that hostel
        # out_params=[None]*19
        # self.cursor.callproc('get_all_student_data_through_hostel',[self.hostel_id[0]]+out_params)
        # result = self.cursor.stored_results()

        # print(result)

        # if result:
        #     # Fetch all rows from the result set
        #     rows = result.fetchall()

        #     # Iterate through each row and insert into the treeview
        #     for row in rows:
        #         self.student_tree.insert('', tk.END, values=row)
        #----------------------------------------------------------------

        # print(self.hostel_id)
        # results =self.cursor.callproc('get_all_student_data_through_hostel2',[self.hostel_id[0]])
        # # results = self.cursor.stored_results()
        # print('line 52')
        # print(results)

        print(self.hostel_id)
        query = f"call get_all_student_data_through_hostel2({self.hostel_id[0]});"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        print(result)

        # Iterate through each row and insert into the treeview
        for row in result:
            self.student_tree.insert('', tk.END, values=row)

        # Set column headings
        for col in columns:
            self.student_tree.heading(col, text=col)

        # Set column widths
        for col in columns:
            self.student_tree.column(col, width=100)

        self.student_tree.pack(padx=20, pady=40, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.student_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.student_tree.configure(yscrollcommand=scrollbar.set)

        add_student_button = Button(self, text='Add Student', command=self.master.show_add_student, bg='#1a2530', fg='white', border=0, width=20, height=1,
                            font=('Microsoft YaHei UI Light', 14))

        add_student_button.pack(pady=40)

    def update_student_table(self, student_data):
        # Clear existing items in the treeview
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        # Insert new student data into the treeview
        for student in student_data:
            self.student_tree.insert('', 'end', values=student)

class AddStudentWindow(tk.Toplevel):
    def __init__(self, master, add_student_callback):
        super().__init__(master)
        self.title('Add Student')
        

        # Set the size of the window
        self.width = 450
        self.height = 650

        # Calculate the position to center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        # Set the geometry of the window
        self.geometry(f'{self.width}x{self.height}+{x}+{y}')

        self.add_student_callback = add_student_callback

        self.connection = mysql.connector.connect(**db_config_manager)
        self.cursor=self.connection.cursor()

        self.hostel_id=-1
        query =f"select hid from manager where mid={config.current_user_id[0]}"
        self.cursor.execute(query)
        self.hostel_id=self.cursor.fetchone()
        
        self.cursor.execute("Select dname from department;")
        self.departments=self.cursor.fetchall()
        self.create_widgets()

    def create_widgets(self):
        # Create entry fields for student information
        labels = ['CMS', 'Password','First Name', 'Last Name', 'Room Number', 'Age', 'Email', 'Phone Number', 'City', 'Street', 'House Number',
                  'Batch', 'Department', 'Program']
        self.entry_fields = {}

        for label in labels:
            tk.Label(self, text=label).pack()
            if label == 'Department':
                # Create a dropdown menu for departments
                entry = ttk.Combobox(self, values=self.departments, state="readonly")
            else:
                entry = Entry(self)
            entry.pack()
            self.entry_fields[label] = entry

        # Add a button to save the student
        save_button = Button(self, text='Save', command=self.save_student, bg='#1a2530', fg='white', border=0,
                             font=('Microsoft YaHei UI Light', 12))
        save_button.pack(pady=20)

        
    def save_student(self):
        # Retrieve data from entry fields and call the callback to add the student
        student_data = {label: entry.get() for label, entry in self.entry_fields.items()}
        print("Switching to Adding student:")
        print(student_data)


        cms, password, firstName, lastName, roomNumber, age, email, phoneNumber, city, street, houseNumber, batch, departmentName, program = student_data.values()
        print(cms,departmentName)
        # Get department ID from dname
        self.cursor.execute(f"SELECT dID FROM Department WHERE dname = '"+departmentName+"';")
        department_id = self.cursor.fetchone()  # Fetch the first column value
        print(department_id)

        # Adding into the student table
        query = '''
            INSERT INTO Student(cms, sFirstName, sLastName, sAge, sEmail, sPhoneNumber, city, street, house_no, sRoomNumber,
                                sBatch, sPassword, sProgram, HID, dID) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        student_values = (
            cms, firstName, lastName, age, email, phoneNumber, city, street,
            houseNumber, roomNumber, batch, password, program, self.hostel_id[0], department_id[0]
        )
        print(student_values)

        try:
            self.cursor.execute(query, student_values)
            print(self.cursor.fetchall())
            self.connection.commit()
            print("Student added successfully!")
            # Call the callback function to update the treeview in the AdminStudent class
            self.add_student_callback(student_data)
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        self.destroy()