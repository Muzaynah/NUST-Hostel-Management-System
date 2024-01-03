import tkinter as tk
from tkinter import ttk, Entry, Button, Toplevel, StringVar, Radiobutton, Scrollbar, LEFT, RIGHT, Y,messagebox
import random
from config import db_config_manager
import config
import mysql.connector
from datetime import datetime,timedelta

class AdminAttendance(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.connection = mysql.connector.connect(**db_config_manager)
        self.cursor = self.connection.cursor()
        # self.current_date_index = 0
        #get current date
        query="select current_date()"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.current_date = result[0][0]
        self.todays_date = result[0][0]
        # print(datetime.now())
        # print(result)
        # print(result[0])
        # print(result[0][0])
        date_object = datetime.strptime(str(result[0][0]), '%Y-%m-%d')
        self.current_year = date_object.year
        self.current_month=date_object.month
        self.current_day=date_object.day
        self.status_text=tk.StringVar()
        self.first_click = False

        #getting hostel id of the logged in manager
        query =f"select hid from manager where mid={config.current_user_id[0]}"
        self.cursor.execute(query)
        self.hostel_id=self.cursor.fetchone()

        self.dates=[result[0]]
        # print(self.dates)
        self.attendance_data = {}
        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        self.date_var = StringVar()
        date_label = ttk.Label(center_frame, textvariable=self.date_var, font=('Helvetica', 12), style='Header.TLabel')
        date_label.pack(pady=(20, 10))
        self.date_var.set(self.current_date)


        #label that shows whether attendance for that day is marked/unmarked
        self.status_label = tk.Label(center_frame, textvariable=self.status_text, font=('Helvetica', 12), bg='white',fg='green')
        self.status_label.pack()
        self.status_text.set("Attendance Status: ")

        #setting up the treeview
        columns = ('CMS ID','Student Name', 'Phone Number','Room Number','Status')
        self.attendance_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        for col in columns:
            self.attendance_tree.heading(col, text=col)

        self.attendance_tree.column('Student Name', width=100)
        self.attendance_tree.column('Status', width=100)

        self.attendance_tree.pack(padx=20, pady=(0, 20), side=tk.TOP, fill=tk.BOTH, expand=True)

        left_button = Button(center_frame, text='<', command=self.show_previous_date, bg='#1a2530', fg='white', border=0,
                             width=2, height=1, font=('Helvetica', 12))
        left_button.pack(side=tk.LEFT, padx=10)

        right_button = Button(center_frame, text='>', command=self.show_next_date, bg='#1a2530', fg='white', border=0,
                              width=2, height=1, font=('Helvetica', 12))
        right_button.pack(side=tk.RIGHT, padx=10)

        self.show_current_date()

        self.take_attendance_button = Button(self, text='Take Attendance', command=self.show_take_attendance_window,
                                              bg='#1a2530', fg='white', border=0, width=20, height=1, font=('Helvetica', 12))
        self.take_attendance_button.pack(pady=20)


    def show_previous_date(self):
        self.attendance_tree.delete(*self.attendance_tree.get_children())
        # if self.current_date_index > 0:
        # #     self.current_date_index -= 1
        # previous_date = current_datetime - timedelta(days=1)
        date_object = datetime.strptime(str(self.current_date), '%Y-%m-%d').date()
        self.current_date = date_object-timedelta(days=1)
        self.show_current_date()

    def show_next_date(self):
        self.attendance_tree.delete(*self.attendance_tree.get_children())
        date_object = datetime.strptime(str(self.current_date), '%Y-%m-%d').date()
        self.current_date = date_object+timedelta(days=1)
        self.show_current_date()

    def show_current_date(self):
        connection = mysql.connector.connect(**db_config_manager)
        cursor=connection.cursor()
        self.date_var.set(f'Date: {self.current_date}')
        # self.update_attendance_table(current_date)
        
        #check if date exists in database
        query = f"SELECT aDate FROM attendanceevent;"
        cursor.execute(query)
        results=cursor.fetchall()
        # print(self.current_date,results)
        # for result in results:
        #     date_tuple = result[0]  # Extract the date tuple from the result tuple
        #     result = datetime.strptime(str(date_tuple), '%Y-%m-%d')
        #     # result = date_tuple.strftime('%Y-%m-%d')
        results = [result[0].strftime('%Y-%m-%d') for result in results]
        date_object = datetime.strptime(str(self.current_date), '%Y-%m-%d').date()
        # print(results,date_object)
        if str(date_object) in results:
            print('line 111')
            #execute queries to fetch data
            query = f'''SELECT cms,CONCAT(sFirstName, ' ',sLastName), sPhoneNumber,sRoomNumber,attendance 
                        FROM StudentGuardiansAttendanceView
                        WHERE ADate = "{date_object}";
            '''
            cursor.execute(query)
            results= cursor.fetchall()
            # print(results)
            if(results):
                for result in results:
                    self.attendance_tree.insert('',tk.END,values=result)
            if(self.current_date == self.todays_date):
                self.status_text.set("Attendance Status: In Progress")
            else:
                self.status_text.set("Attendance Status: Marked (Immutable)")
        else:
            print('line 124')
            self.status_text.set("Attendance Status: Unmarked")

            #insert data of all students without the attendance status
            query = f"call get_all_student_data_through_hostel2({self.hostel_id[0]})"
            cursor.execute(query)
            results=cursor.fetchall()
            # print(results)
            for result in results:
                cms,firstName,lastName,age,email,phoneNumber,city,street,house_no,roomNumber,batch,dept_id,dept_name,program,hostel_id,hostel_name = result
                values = [cms,firstName + ' '+ lastName,phoneNumber,roomNumber]
                # if(results):
                #     for result in results:
                self.attendance_tree.insert('',tk.END,values=values+['NULL'])

    def show_take_attendance_window(self):
        connection = mysql.connector.connect(**db_config_manager)
        cursor = connection.cursor()

        if(self.current_date == self.todays_date):
            #get names of students from the tree
            name_column = []
            for item in self.attendance_tree.get_children():
                values = self.attendance_tree.item(item, 'values')
                if values:
                    first_column_value = values[1]
                    cms_value = values[0]
                    status_value = values[4]
                    name_column.append([cms_value,first_column_value,status_value])
            self.status_text.set("Attendance Status: In Progress")

            #insert data into attendance event with attendance as absent
            if(self.first_click==False):
                self.first_click=True
                #get all students cms
                query = f"select DISTINCT cms FROM StudentGuardiansAttendanceView where StudentHostelID = {self.hostel_id[0]}"
                cursor.execute(query)
                cms_results=cursor.fetchall()
                for cms in cms_results:
                    #check if cms already exists
                    check_query = f"SELECT COUNT(*) FROM attendanceevent WHERE cms = {cms[0]} AND ADate = '{self.current_date.strftime('%Y-%m-%d')}'"
                    cursor.execute(check_query)
                    count = cursor.fetchone()[0]

                    if count == 0:
                        #insert if it doesnt already exist
                        insert_query = f"INSERT INTO attendanceevent(ADate, Attendance, cms) VALUES ('{self.current_date.strftime('%Y-%m-%d')}', 'Absent', {cms[0]})"
                        cursor.execute(insert_query)
                        connection.commit()

            take_attendance_window = AttendanceEditorWindow(self, self.current_date, name_column,self.current_date,self.attendance_tree,self.show_current_date)
            
        else:
            messagebox.showerror("Error","You can't take the attendance for this day.")



class AttendanceEditorWindow(tk.Toplevel):
    def __init__(self, take_attendance_window, date, attendance_data,current_date,attendance_tree,show_current_date):
        super().__init__(take_attendance_window)
        self.title('Attendance Editor')
        self.take_attendance_window = take_attendance_window
        self.date = date
        self.attendance_data = attendance_data
        self.student_vars = []  # Store student and status variables
        self.current_date = current_date
        # print(self.current_date)
        # print(self.date)
        self.attendance_tree = attendance_tree
        self.show_current_date=show_current_date

        self.create_widgets()

    def create_widgets(self):

        # Create a frame to hold the student attendance widgets and scrollbar
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to hold the frame and attach the scrollbar
        canvas = tk.Canvas(frame)
        canvas.pack(side=LEFT, fill=tk.BOTH, expand=True)

        # Attach scrollbar to the canvas
        scrollbar = Scrollbar(frame, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create another frame to hold the student attendance widgets
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Create student attendance widgets
        for cms,student, status in self.attendance_data:
            student_frame = tk.Frame(inner_frame)
            student_frame.pack(side=tk.TOP, pady=5)

            cms_var = StringVar(value=cms)
            tk.Label(student_frame, textvariable=cms_var, width=5, anchor='w').pack(side=LEFT)

            student_var = StringVar(value=student)
            tk.Label(student_frame, textvariable=student_var, width=17, anchor='w').pack(side=LEFT)

            # Set the default status to "Absent" if the status is an empty string
            default_status = 'Absent' if status == '' or status == 'NULL' else status
            status_var = StringVar(value=default_status)

            Radiobutton(student_frame, text='Absent', variable=status_var, value='Absent').pack(side=LEFT)
            Radiobutton(student_frame, text='Present', variable=status_var, value='Present').pack(side=LEFT)
            Radiobutton(student_frame, text='Leave', variable=status_var, value='Leave').pack(side=LEFT)

            # Store student and status variables
            self.student_vars.append((cms_var, status_var))

        # Add the Save button
        save_button = Button(inner_frame, text='Save', command=lambda:self.save_attendance(self.show_current_date), bg='#1a2530', fg='white', border=0,
                             font=('Helvetica', 12))
        save_button.pack(pady=20)

        # Update the scroll region of the canvas
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def save_attendance(self,show_current_date):

        connection = mysql.connector.connect(**db_config_manager)
        cursor = connection.cursor()

        #update the attendance for every student
        # #get cms of every student first
        # query = "select DISTINCT cms FROM StudentGuardiansAttendanceView"
        # cursor.execute(query)
        # cms_results=cursor.fetchall()
        for cms_var, status_var in self.student_vars:
            cms = cms_var.get()  # Get the value from StringVar
            status = status_var.get()  # Get the value from StringVar
            # print(cms,status)
            query = f"UPDATE AttendanceEvent SET Attendance = '{status}' WHERE cms = {cms} AND ADate = '{self.current_date.strftime('%Y-%m-%d')}'"
            cursor.execute(query)
            connection.commit()
            
        
        #resetting the treeview and updating
        self.attendance_tree.delete(*self.attendance_tree.get_children())
        # self.show_current_date()
        show_current_date()

        self.destroy()  # Close the AttendanceEditorWindow
