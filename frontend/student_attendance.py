import tkinter as tk
from tkinter import Button, Entry, Label, Listbox, Scrollbar, StringVar, OptionMenu, messagebox,ttk
from datetime import datetime
import mysql.connector
from config import db_config_student
import config

class StudentAttendance(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.connection = mysql.connector.connect(**db_config_student)
        self.cursor = self.connection.cursor()
        # self.view_name = str(config.current_user_id[0]) + '_student'
        self.attendance_tree = ttk.Treeview(self, columns=('Date', 'Status'), show='headings', height=15)
        if(config.current_user_id != -1):
            self.create_widgets()

    def create_widgets(self):

        # Title label
        title_label = Label(self, text='Attendance Record', font=('Helvetica', 16))
        title_label.pack(pady=20)

        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self, width=600, height=600, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Filter options
        # date_label = Label(right_frame, text='Date:')
        # date_label.pack(pady=(0, 5))
        # self.date_entry = Entry(right_frame)
        # self.date_entry.pack(pady=(0, 10))

        # Date label
        date_label = Label(right_frame, text='Date:', font=('Microsoft YaHei UI Light', 12), bg='white')
        date_label.pack()

        # Date dropdowns
        self.day_var = StringVar()
        self.month_var = StringVar()
        self.year_var = StringVar()

        day_menu = ttk.Combobox(right_frame, textvariable=self.day_var, values=["Day"] + list(range(1, 32)), state="readonly")
        month_menu = ttk.Combobox(right_frame, textvariable=self.month_var, values=["Month"] + list(range(1, 13)), state="readonly")
        year_menu = ttk.Combobox(right_frame, textvariable=self.year_var, values=["Year"] + list(range(datetime.now().year, datetime.now().year + 1)), state="readonly")
        
        #default values
        self.day_var.set("Day")
        self.month_var.set("Month")
        self.year_var.set("Year")

        day_menu.pack()
        month_menu.pack()
        year_menu.pack()

        self.status_options = ["All", "Present", "Absent"]
        self.status_label = Label(right_frame, text='Status:', font=('Microsoft YaHei UI Light', 12), bg='white')
        self.status_label.pack(pady=5)
        self.status_var = StringVar()
        self.status_var.set(self.status_options[0])

        self.status_menu = ttk.Combobox(right_frame, textvariable=self.status_var, values=self.status_options, state="readonly")
        # self.status_menu.bind('<<ComboboxSelected>>', lambda _: self.filter_complaints(self.complaint_tree, self.filter_var.get()))
        self.status_menu.pack(pady=10)

        self.status_var.set(self.status_options[0])

        # Filter and Reset buttons
        filter_button = Button(right_frame, text='Filter', command=self.apply_filters)
        filter_button.pack(pady=10)

        reset_button = Button(right_frame, text='Reset', command=self.reset_filters)
        reset_button.pack(pady=10)

        # Treeview to display attendance records------------------------------------------------------------

        #gets the current users attendance logs
        # print('line 59 student_attendance')
        query = f"call get_attendance_data({config.current_user_id[0]})"
        self.cursor.execute(query, multi=True)
        results = self.cursor.fetchall()
        
        if(results):
            #insert each row of attendance record into the treeview
            for result in results:
                self.attendance_tree.insert('',tk.END,values=result)

        # self.attendance_tree = ttk.Treeview(left_frame, columns=('Date', 'Status'), show='headings', height=15)
        self.attendance_tree.heading('Date', text='Date')
        self.attendance_tree.heading('Status', text='Status')
        self.attendance_tree.pack(padx=10,pady=10)

        # sample data
        # attendance_data = [("2023-01-01", "Present"), ("2023-01-02", "Absent"), ("2023-01-03", "Present")]
        # for item in attendance_data:
        #     self.attendance_tree.insert('', tk.END, values=item)

        #----------------------------------------------------------------------------------------------------

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.attendance_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.attendance_tree.config(yscrollcommand=scrollbar.set)

    def apply_filters(self):

        #resetting the tree first 
        self.attendance_tree.delete(*self.attendance_tree.get_children())

        connection = mysql.connector.connect(**db_config_student)
        cursor = connection.cursor()
        #get all data first
        query = f"call get_attendance_data({config.current_user_id[0]})"
        cursor.execute(query, multi=True)
        results = cursor.fetchall()
        
        if(results):
            for result in results:
                self.attendance_tree.insert('',tk.END,values=result)
        
        #the filtering part
        items=self.attendance_tree.get_children()
        print(items)
        #by date
        new_day = self.day_var.get()
        if(new_day!="Day"):
            i=0
            for item in items:
                print(item)
                item_values = self.attendance_tree.item(item,'values')
                date_object = datetime.strptime(item_values[0], '%Y-%m-%d')
                year = date_object.year
                month=date_object.month
                day=date_object.day
                print(new_day,day)
                if(new_day != str(day)): 
                    self.attendance_tree.delete(item)
        new_month = self.month_var.get()
        items=self.attendance_tree.get_children()
        if(new_month!="Month"):
            for item in items:
                print(item)
                item_values = self.attendance_tree.item(item,'values')
                date_object = datetime.strptime(item_values[0], '%Y-%m-%d')
                year = date_object.year
                month=date_object.month
                day=date_object.day
                print(new_month,month)
                if(new_month!=str(month)):
                    print('deleting ',item)
                    self.attendance_tree.delete(item)
                    
        new_year = self.year_var.get()
        items=self.attendance_tree.get_children()
        if(new_year!="Year"):
            for item in items:
                item_values = self.attendance_tree.item(item,'values')
                date_object = datetime.strptime(item_values[0], '%Y-%m-%d')
                year = date_object.year
                month=date_object.month
                day=date_object.day
                print(new_year,year)
                if(new_year != str(year)):
                    self.attendance_tree.delete(item)

        #by status
        new_status = self.status_var.get()
        items=self.attendance_tree.get_children()
        if(new_status!="All"):
            for item in items:
                item_values = self.attendance_tree.item(item,'values')
                status = item_values[1]
                print(new_status,status)
                if(new_status != status):
                    self.attendance_tree.delete(item)

    def reset_filters(self):
        connection = mysql.connector.connect(**db_config_student)
        cursor=connection.cursor()

        self.day_var.set("Day")
        self.month_var.set("Month")
        self.year_var.set("Year")
        self.status_var.set('All')

        # Reset the treeview to show all data (replace with actual data retrieval)
        # all_data = [("2023-01-01", "Present"), ("2023-01-02", "Absent"), ("2023-01-03", "Present")]

        query = f"call get_attendance_data({config.current_user_id[0]})"
        cursor.execute(query)
        results = cursor.fetchall()

        # Clear existing treeview items
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)

        # Insert all data into the treeview
        for item in results:
            self.attendance_tree.insert('', tk.END, values=item)

    def get_filtered_data(self, selected_date, selected_status):
        # Placeholder function to simulate data retrieval based on filters
        # Replace this with actual database queries based on the selected filters
        # For simplicity, returning dummy data
        if(selected_date == 'All' and selected_status == "All"):
            query = f"call get_attendance_data({config.current_user_id[0]})"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        elif(selected_status == 'All'):
            query = f"call get_attendance_data_through_date({config.current_user_id},{selected_date});"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        elif(selected_date == 'All'):
            query = f"call get_attendance_data_through_attendance({config.current_user_id},{selected_status});"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        else:
            query = f"call get_attendance_data_through_attendance_date({config.current_user_id},{selected_status},{selected_date})"
            self.cursor.execute(query)
            results = self.cursor.fetchall()
        return results
