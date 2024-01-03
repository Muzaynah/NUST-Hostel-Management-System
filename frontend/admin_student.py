import tkinter as tk
from tkinter import Label, Button, PhotoImage, ttk, Entry, Toplevel,messagebox
import mysql.connector
from config import db_config_manager
import config

class AdminStudent(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.connection=mysql.connector.connect(**db_config_manager)
        self.cursor=self.connection.cursor()
        self.con1=mysql.connector.connect(**db_config_manager)
        self.cursor1=self.con1.cursor()
        self.hostel_id=-1
        self.create_widgets()

    def create_widgets(self):

        # Create a frame to center the treeview
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        Label(center_frame, text="Student's Information", font=('Microsoft YaHei UI Light', 20, 'bold'), bg='white', fg = 'black').pack(pady=30)


        # Create a treeview for displaying students
        columns = ('CMS', 'First Name', 'Last Name', 'Age', 'Email', 'Phone Number', 'City', 'Street', 'House Number', 'Room Number','Batch','Department ID', 'Department Name', 'Program','Hostel ID','Hostel Name','Guardian 1 Name','Guardian 1 Phone Number','Guardian 1 Email','Guardian 2 Name','Guardian 2 Phone Number','Guardian 2 Email','Guardian 3 Name','Guardian 3 Phone Number','Guardian 3 Email')
        self.student_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        #adding scrollbar to treeview
        scrollbar = ttk.Scrollbar(self.student_tree, orient="horizontal", command=self.student_tree.xview)

        # Configure the Treeview to use the scrollbar
        self.student_tree.configure(xscrollcommand=scrollbar.set)

        # Place the scrollbar on the right side of the Treeview
        scrollbar.pack(side="bottom", fill="x")

        #getting initial data for treeview-----------------------------------

        #getting hostel id of the logged in manager
        query =f"select hid from manager where mid={config.current_user_id[0]}"
        self.cursor.execute(query)
        self.hostel_id=self.cursor.fetchone()
    
        #getting student data
        print(self.hostel_id)
        query = f"call get_all_student_data_through_hostel2({self.hostel_id[0]});"
        self.cursor.execute(query, multi=True)
        result = self.cursor.fetchall()
        print(result)


        # Iterate through each row and insert into the treeview
        for row in result:
            cms = row[0]
            
            #getting guardian data for every student
            query = f"select gName, gPhoneNumber,gEmail FROM Guardian WHERE cms={cms}"
            self.cursor1.execute(query)
            guardian_result =  self.cursor1.fetchall()
            print(guardian_result)
            
            #concatenate the 3 guardians with the row array
            for i in range(len(guardian_result)):
                if(guardian_result[i]):
                    row = row + guardian_result[i]

            self.student_tree.insert('', tk.END, values=row)

        # Set column headings
        for col in columns:
            self.student_tree.heading(col, text=col)

        # Set column widths
        for col in columns:
            self.student_tree.column(col, width=100)

        self.student_tree.pack(padx=20, pady=40, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self.student_tree, orient='vertical', command=self.student_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.student_tree.configure(yscrollcommand=scrollbar.set)

        add_student_button = Button(self, text='Add Student', command=self.show_add_student_window, bg='#1a2530', fg='white', border=0, width=20, height=1,
                            font=('Microsoft YaHei UI Light', 14))

        add_student_button.pack(pady=40)
    
    def show_add_student_window(self):
        connection= mysql.connector.connect(**db_config_manager)
        cursor = connection.cursor()
        print("Adding student:")
        self.add_student_window = AddStudentWindow(self,self.student_tree)




class AddStudentWindow(tk.Toplevel):
    def __init__(self, master,student_tree):
        super().__init__(master)
        self.title('Add Student')
        self.student_tree=student_tree
        

        # Set the size of the window
        self.width = 450
        self.height = 600

        # Calculate the position to center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        # Set the geometry of the window
        self.geometry(f'{self.width}x{self.height}+{x}+{y}')

        # self.add_student_callback = add_student_callback

        self.canvas = tk.Canvas(self)
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Create a Frame inside the Canvas to hold the widgets
        self.scrollable_frame = tk.Frame(self.canvas)
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Add the Frame to the Canvas
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


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
                  'Batch', 'Department', 'Program','Guardian 1 Name','Guardian 1 Phone Number','Guardian 1 Email','Guardian 2 Name','Guardian 2 Phone Number','Guardian 2 Email','Guardian 3 Name','Guardian 3 Phone Number','Guardian 3 Email']
        self.entry_fields = {}

        for label in labels:
            entry_frame = tk.Frame(self.scrollable_frame)  # Create a frame for each label and entry
            entry_frame.pack(fill=tk.X, padx=100, pady=5)  # Pack the frame horizontally with padding

            tk.Label(entry_frame, text=label).pack(side=tk.LEFT)  # Pack the label to the left inside the entry_frame

            if label == 'Department':
                # Create a dropdown menu for departments
                entry = ttk.Combobox(entry_frame, values=self.departments, state="readonly")
                entry.pack(side=tk.RIGHT)  # Pack the entry to the right inside the entry_frame
            else:
                entry = Entry(entry_frame)
                entry.pack(side=tk.RIGHT)  # Pack the entry to the right inside the entry_frame

            self.entry_fields[label] = entry

        # Add a button to save the student
        save_button = Button(self.scrollable_frame, text='Save', command=self.save_student, bg='#1a2530', fg='white', border=0,
                             font=('Microsoft YaHei UI Light', 12))
        save_button.pack(pady=20)

        
    def save_student(self):
        connection =mysql.connector.connect(**db_config_manager)
        cursor=connection.cursor()
        # Retrieve data from entry fields and call the callback to add the student
        student_data = {label: entry.get() for label, entry in self.entry_fields.items()}
        print("Switching to Adding student:")
        print(student_data)


        cms, password, firstName, lastName, roomNumber, age, email, phoneNumber, city, street, houseNumber, batch, departmentName, program, g1_name, g1_phone_number,g1_email, g2_name, g2_phone_number,g2_email, g3_name, g3_phone_number,g3_email= student_data.values()
        if(len(str(cms))!=6):
            messagebox.showerror("Error","CMS should be 6 digits long.")
            return
        if('@' not in email or '@' not in g1_email or '@' not in g2_email or '@' not in g3_email):
            messagebox.showerror("Error","Invalid Email.")
            return
        # Get department ID from dname
        cursor.execute(f"SELECT dID FROM Department WHERE dname = '"+departmentName+"';")
        department_id = cursor.fetchone()  # Fetch the first column value

        # Adding into the student table
        query1 = '''
            INSERT INTO Student(cms, sFirstName, sLastName, sAge, sEmail, sPhoneNumber, city, street, house_no, sRoomNumber,
                                sBatch, sPassword, sProgram, HID, dID) 
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        '''

        student_values = (
            cms, firstName, lastName, age, email, phoneNumber, city, street,
            houseNumber, roomNumber, batch, password, program, self.hostel_id[0], department_id[0]
        )
        print(student_values)


        if(g2_name==''):
            g2_name='NULL'
        if(g2_phone_number==''):
            g2_phone_number='NULL'
        if(g2_email==''):
            g2_email='NULL'
        if(g3_name==''):
            g3_name='NULL'
        if(g3_phone_number==''):
            g3_phone_number='NULL'
        if(g3_email==''):
            g3_email='NULL'
        #adding in the guardians
        print(g1_name,g1_phone_number,g1_email)
        query2 = f'''INSERT INTO Guardian(gName,gPhoneNumber,gEmail,cms) 
                VALUES('{g1_name}',{g1_phone_number},'{g1_email}',{cms}),
                        ('{g2_name}',{g2_phone_number},'{g2_email}',{cms}),
                        ('{g3_name}',{g3_phone_number},'{g3_email}',{cms});
                        '''
        
        try:
            cursor.execute(query1, student_values)
            print(self.cursor.fetchall())
            connection.commit()
            cursor.execute(query2)
            connection.commit()
            print("Student added successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

        #resetting the tree
        self.student_tree.delete(*self.student_tree.get_children())

        #getting student data
        print(self.hostel_id)
        query = f"call get_all_student_data_through_hostel2({self.hostel_id[0]});"
        self.cursor.execute(query, multi=True)
        result = self.cursor.fetchall()
        print(result)

        # Iterate through each row and insert into the treeview
        for row in result:
            cms = row[0]
            
            #getting guardian data for every student
            query = f"select gName, gPhoneNumber,gEmail FROM Guardian WHERE cms={cms}"
            cursor.execute(query)
            guardian_result =  cursor.fetchall()
            print(guardian_result)
            
            #concatenate the 3 guardians with the row array
            for i in range(len(guardian_result)):
                if(guardian_result[i]):
                    row = row + guardian_result[i]

            self.student_tree.insert('', tk.END, values=row)

        

        self.destroy()