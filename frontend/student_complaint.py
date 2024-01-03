import tkinter as tk
from tkinter import Button, Label, Text, StringVar, messagebox, ttk
from datetime import datetime
import mysql.connector
from config import db_config_student
import config

class StudentComplaint(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.complaint_data = []
        self.connection = mysql.connector.connect(**db_config_student)
        self.cursor = self.connection.cursor()
        self.create_widgets()

    def create_widgets(self):
        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        right_frame = tk.Frame(self, width=800, height=600, bg='white') 
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File New Complaint Section
        new_complaint_label = Label(left_frame, text='File New Complaint', font=('Microsoft YaHei UI Light', 18, 'bold'), bg='white', fg = 'black')
        new_complaint_label.pack(pady=(20))

        # Text field for new complaint
        self.complaint_text = Text(left_frame, width=30, height=10, font=('Microsoft YaHei UI Light', 12))
        self.complaint_text.pack(pady=(0, 10))
        self.complaint_text.insert(tk.END, 'Write complaint detail here')
        self.complaint_text.bind("<FocusIn>", self.on_text_focus)
        self.complaint_text.bind("<FocusOut>", self.on_text_focus_out)

        # # Date label
        # date_label = Label(left_frame, text='Date:', font=('Microsoft YaHei UI Light', 12), bg='white')
        # date_label.pack()

        # # Date dropdowns
        # self.leaving_day_var = StringVar()
        # self.leaving_month_var = StringVar()
        # self.leaving_year_var = StringVar()

        # day_menu = ttk.Combobox(left_frame, textvariable=self.leaving_day_var, values=["Day"] + list(range(1, 32)), state="readonly")
        # month_menu = ttk.Combobox(left_frame, textvariable=self.leaving_month_var, values=["Month"] + list(range(1, 13)), state="readonly")
        # year_menu = ttk.Combobox(left_frame, textvariable=self.leaving_year_var, values=["Year"] + list(range(datetime.now().year, datetime.now().year + 1)), state="readonly")

        # day_menu.pack()
        # month_menu.pack()
        # year_menu.pack()

        # Submit and Reset Buttons
        submit_button = Button(left_frame, text='Submit', command=self.submit_complaint,
                               font=('Microsoft YaHei UI Light', 12), bg='#1a2530', fg='white', border=0, width=20, height=1)
        submit_button.pack(pady=(30,5))

        reset_button = Button(left_frame, text='Reset', command=self.reset_fields,
                              font=('Microsoft YaHei UI Light', 12), bg='#1a2530', fg='white', border=0, width=20, height=1)
        reset_button.pack(pady=10)

        # Complaint History Section
        Label(right_frame, text='Complaint Log', font=('Microsoft YaHei UI Light', 18, 'bold'), fg = 'black', bg='white').pack(pady=20)

        # Complaint Treeview

        columns = ('Complaint ID', 'Date', 'Description', 'Status')
        self.complaint_tree = ttk.Treeview(right_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.complaint_tree.heading(col, text=col)
        self.complaint_tree.pack(pady=10)

        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=self.complaint_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.complaint_tree.config(yscrollcommand=scrollbar.set)

        #fetching data
        # results = self.cursor.callproc('get_complaint_data_through_cms',[config.current_user_id[0]])
        query =f"call get_complaint_data_through_cms({config.current_user_id[0]})"
        self.cursor.execute(query,multi=True)
        results=self.cursor.fetchall()
        for result in results:
            self.complaint_tree.insert('',tk.END,values=result)
        # print('line 83 in student_complaint',results)
        
        # Filter Options
        self.filter_options = ["All", "In Progress", "Resolved", "Pending"]
        self.filter_label = Label(right_frame, text='Filter Complaints:', font=('Microsoft YaHei UI Light', 12), bg='white')
        self.filter_label.pack(pady=5)
        self.filter_var = StringVar()
        self.filter_var.set(self.filter_options[0])

        self.filter_menu = ttk.Combobox(right_frame, textvariable=self.filter_var, values=self.filter_options, state="readonly")
        self.filter_menu.bind('<<ComboboxSelected>>', lambda _: self.filter_complaints(self.complaint_tree, self.filter_var.get()))
        self.filter_menu.pack(pady=10)

        reset_button = Button(right_frame, text='Reset', command=lambda: self.filter_complaints(self.complaint_tree, "All"),
                              font=('Microsoft YaHei UI Light', 12), bg='#1a2530', fg='white', border=0, width=10, height=1)
        reset_button.pack(pady=5)

    def submit_complaint(self):
        description = self.complaint_text.get("1.0", "end-1c")
        if not description.strip():
            messagebox.showerror("Error", "Complaint field must be filled.")
            return

        # leaving_date = datetime(int(self.leaving_year_var.get()), int(self.leaving_month_var.get()), int(self.leaving_day_var.get()))

        # complaint_data = ("Complaint {}".format(len(self.complaint_data) + 1), leaving_date.strftime("%Y-%m-%d"), description, "Pending")
        # self.complaint_data.append(complaint_data)

        # self.update_complaint_tree()
        self.insert_complaint_into_db(description, "Pending")

        success_window = tk.Toplevel(self.master)
        success_window.title("Success")

        success_label = Label(success_window, text="Complaint submitted successfully!")
        success_label.pack(padx=20, pady=20)

        ok_button = Button(success_window, text="OK", command=success_window.destroy)
        ok_button.pack(pady=10)

        window_width = success_window.winfo_reqwidth()
        window_height = success_window.winfo_reqheight()

        screen_width = success_window.winfo_screenwidth()
        screen_height = success_window.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        success_window.geometry("+{}+{}".format(x_position, y_position))

        # Reset fields after submission
        self.reset_fields()

    def insert_complaint_into_db(self, description, status):
        connection = mysql.connector.connect(**db_config_student)
        cursor=connection.cursor()
        insert_query = """
        INSERT INTO Complaint (CDescription, CStatus, CDate, cms)
        VALUES (%s, %s, current_date(), %s);
        """
        cms_id = config.current_user_id[0]
        data = (description, status, cms_id)

        try:
            cursor.execute(insert_query, data)
            connection.commit()
            print("Complaint inserted into the database successfully!")

        except Exception as e:
            print(f"Error: {e}")
        
        #reset the tree and fetch it again to get updated the tree
        self.complaint_tree.delete(*self.complaint_tree.get_children())

        query =f"call get_complaint_data_through_cms({config.current_user_id[0]})"
        cursor.execute(query,multi=True)
        results=cursor.fetchall()
        for result in results:
            self.complaint_tree.insert('',tk.END,values=result)

    def filter_complaints(self, treeview, status):

        connection = mysql.connector.connect(**db_config_student)
        cursor=connection.cursor()

        treeview.delete(*treeview.get_children())

        #running queries for complaints 
        query =f"call get_complaint_data_through_cms({config.current_user_id[0]})"
        cursor.execute(query,multi=True)
        results=cursor.fetchall()
        for result in results:
            self.complaint_tree.insert('',tk.END,values=result)
        
        if(status=="All"): 
            self.filter_menu.set(self.filter_options[0])
            return

        #the filtering part
        items = self.complaint_tree.get_children()
        print('line 180: ',items)
        for item in items:
            #get their values
            item_values = self.complaint_tree.item(item,'values')
            print('line 184: ',item_values)

            if(item_values[3] != status):
                self.complaint_tree.delete(item)
        
        items = []
        for child in self.complaint_tree.get_children():
            item = self.complaint_tree.item(child)
            items.append(item['values'])
        return items

    def reset_fields(self):
      
        self.complaint_text.delete('1.0', tk.END)
        self.complaint_text.insert(tk.END, 'Write complaint detail here')
        self.on_text_focus(None)  # Manually trigger the focus event

    def on_text_focus(self, event):
        if self.complaint_text.get("1.0", "end-1c") == 'Write complaint detail here':
            self.complaint_text.delete("1.0", "end-1c")

    def on_text_focus_out(self, event):
        if not self.complaint_text.get("1.0", "end-1c").strip():
            self.complaint_text.insert(tk.END, 'Write complaint detail here')
