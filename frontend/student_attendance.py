import tkinter as tk
from tkinter import Button, Entry, Label, Listbox, Scrollbar, StringVar, OptionMenu, messagebox,ttk
from datetime import datetime
import mysql.connector
from config import db_config_student
import config

class StudentAttendance(tk.Frame):
    def __init__(self, master, show_dashboard):
        super().__init__(master)
        self.master = master
        self.show_dashboard = show_dashboard
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
        date_label = Label(right_frame, text='Date:')
        date_label.pack(pady=(0, 5))
        self.date_entry = Entry(right_frame)
        self.date_entry.pack(pady=(0, 10))

        status_label = Label(right_frame, text='Status:')
        status_label.pack(pady=(0, 5))
        self.status_var = StringVar(right_frame)
        status_options = ['All', 'Present', 'Absent']
        self.status_var.set(status_options[0])  # Default to 'All'
        status_dropdown = OptionMenu(right_frame, self.status_var, *status_options)
        status_dropdown.pack(pady=(0, 10))

        # Filter and Reset buttons
        filter_button = Button(right_frame, text='Filter', command=self.apply_filters)
        filter_button.pack(pady=10)

        reset_button = Button(right_frame, text='Reset', command=self.reset_filters)
        reset_button.pack(pady=10)

        # Treeview to display attendance records------------------------------------------------------------

        #gets the current users attendance logs
        print('line 59 student_attendance')
        query = f"call get_attendance_data({config.current_user_id[0]})"
        self.cursor.execute(query)
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
        attendance_data = [("2023-01-01", "Present"), ("2023-01-02", "Absent"), ("2023-01-03", "Present")]
        for item in attendance_data:
            self.attendance_tree.insert('', tk.END, values=item)

        #----------------------------------------------------------------------------------------------------

        # Scrollbar for the treeview
        scrollbar = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.attendance_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.attendance_tree.config(yscrollcommand=scrollbar.set)

        # Back to dashboard button
        back_button = Button(self, text='Back to Dashboard', command=self.show_dashboard)
        back_button.pack(pady=20)

    def apply_filters(self):

        # Get filter values
        selected_date = self.date_entry.get()
        selected_status = self.status_var.get()

        # Apply filters to the treeview (replace with actual data retrieval)
        filtered_data = self.get_filtered_data(selected_date, selected_status)

        # Clear existing treeview items
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)

        # Insert filtered data into the treeview
        for item in filtered_data:
            self.attendance_tree.insert('', tk.END, values=item)

    def reset_filters(self):
        # Reset filter fields
        #!!!!!!!!!
        # self.date_entry.set('All')
        self.status_var.set('All')

        # Reset the treeview to show all data (replace with actual data retrieval)
        # all_data = [("2023-01-01", "Present"), ("2023-01-02", "Absent"), ("2023-01-03", "Present")]

        query = f"call get_attendance_data({config.current_user_id[0]})"
        self.cursor.execute(query)
        results = self.cursor.fetchall()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentAttendance(root, show_dashboard=lambda: print("Back to Dashboard"))
    app.pack()
    root.mainloop()