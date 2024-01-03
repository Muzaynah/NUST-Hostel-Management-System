import tkinter as tk
from tkinter import ttk
from tkinter import Button, Entry, Label, Listbox, Scrollbar, StringVar, OptionMenu, messagebox
from datetime import datetime
import mysql.connector
from config import db_config_student
import config

class StudentOutpass(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg = 'white')
        self.master = master
        self.connection=mysql.connector.connect(**db_config_student)
        self.cursor=self.connection.cursor()
        self.outpass_tree = None
        
        self.create_widgets()
        
    def create_widgets(self):

        # Create a frame for the left section (apply for outpass)
        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the right section (outpass log)
        right_frame = tk.Frame(self, width=600, height=600, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Request an outpass section (Left Frame)
        Label(left_frame, text='Request an Outpass', bg = 'white', fg= 'black', font=('Microsoft YaHei UI Light', 16, 'bold')).pack(pady=30)

        # Entry widgets for outpass request form
        purpose_label = Label(left_frame, text='Purpose:', font=('Microsoft YaHei UI Light', 12), bg='white')
        purpose_label.pack(pady=10)
        self.purpose_entry = Entry(left_frame, font=('Microsoft YaHei UI Light', 10))
        self.purpose_entry.pack(pady=(0,10))

        # Leaving Date
        leaving_date_label = Label(left_frame, text='Leaving Date:', font=('Microsoft YaHei UI Light', 12), bg='white')
        leaving_date_label.pack(pady=10)

        # Combo boxes for day, month, and year
        self.day_var = StringVar()
        self.month_var = StringVar()
        self.year_var = StringVar()

        day_menu = ttk.Combobox(left_frame, textvariable=self.day_var, values=["Day"] + list(range(1, 32)), state="readonly", font=('Microsoft YaHei UI Light', 10))
        month_menu = ttk.Combobox(left_frame, textvariable=self.month_var, values=["Month"] + list(range(1, 13)), state="readonly", font=('Microsoft YaHei UI Light', 10))
        year_menu = ttk.Combobox(left_frame, textvariable=self.year_var, values=["Year"] + list(range(datetime.now().year, datetime.now().year + 1)), state="readonly", font=('Microsoft YaHei UI Light', 10))

        # Default values
        self.day_var.set("Day")
        self.month_var.set("Month")
        self.year_var.set("Year")

        day_menu.pack()
        month_menu.pack()
        year_menu.pack()

        # Joining Date
        joining_date_label = Label(left_frame, text='Joining Date:', font=('Microsoft YaHei UI Light', 12), bg='white')
        joining_date_label.pack(pady=(20,10))

        # Combo boxes for day, month, and year
        self.day_var_joining = StringVar()
        self.month_var_joining = StringVar()
        self.year_var_joining = StringVar()

        day_menu_joining = ttk.Combobox(left_frame, textvariable=self.day_var_joining, values=["Day"] + list(range(1, 32)), state="readonly", font=('Microsoft YaHei UI Light', 10))
        month_menu_joining = ttk.Combobox(left_frame, textvariable=self.month_var_joining, values=["Month"] + list(range(1, 13)), state="readonly", font=('Microsoft YaHei UI Light', 10))
        year_menu_joining = ttk.Combobox(left_frame, textvariable=self.year_var_joining, values=["Year"] + list(range(datetime.now().year, datetime.now().year + 1)), state="readonly", font=('Microsoft YaHei UI Light', 10))

        # Default values
        self.day_var_joining.set("Day")
        self.month_var_joining.set("Month")
        self.year_var_joining.set("Year")

        day_menu_joining.pack()
        month_menu_joining.pack()
        year_menu_joining.pack()

        # Submit button
        submit_button = Button(left_frame, text='Submit', command=self.submit_outpass, font=('Microsoft YaHei UI Light', 12), bg='#1a2530', fg='white', border=0)
        submit_button.pack(pady=40)

        # Outpass Log section (Right Frame)

         # Request an outpass section (Left Frame)
        Label(right_frame, text='Outpass Log', bg = 'white', fg= 'black', font=('Microsoft YaHei UI Light', 16, 'bold')).pack(pady=30)
        columns = ("Outpass ID", "Purpose", "Leaving Date", "Joining Date", "Status")
        self.outpass_tree = ttk.Treeview(right_frame, columns=columns, show="headings", selectmode="browse", height=30)

        for col in columns:
            self.outpass_tree.heading(col, text=col)
            self.outpass_tree.column(col, width=100)  # Set the width as needed

        self.outpass_tree.pack(pady=10)

       # Scrollbar for the Treeview
        # scrollbar = Scrollbar(outpass_tree, orient=tk.VERTICAL, command=outpass_tree.yview)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # scrollbarX = Scrollbar(outpass_tree, orient=tk.HORIZONTAL, command=outpass_tree.xview)
        # scrollbarX.pack(side=tk.BOTTOM, fill=tk.X)

        # outpass_tree.config(yscrollcommand=scrollbar.set, xscrollcommand=scrollbarX.set)


        #initializing the outpass treeview with previous values
        # try:

        query = f"call get_outpass_data_through_cms({config.current_user_id[0]})"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        print(results)
        # except mysql.connector.Error as err:
        # messagebox.showerror("Error", f"Database Error: {err}")

        
        # self.outpass_tree.tag_configure('approved_tag', background='light green')

        #self.outpass_tree.tag_configure('approved', background='#a3d9c2')
        # self.outpass_tree.tag_configure('approved', foreground='red')
        #self.outpass_tree.tag_configure('rejected',background='#e8a0a7')

        for result in results:
            if result[4]=='Approved':
                self.outpass_tree.insert('',tk.END,values=result,tags=('approved'))
            elif result[4]=='Rejected':
                self.outpass_tree.insert('',tk.END,values=result,tags=('rejected'))
            else:
                self.outpass_tree.insert('', tk.END, values=result)

    def submit_outpass(self):

        connection = mysql.connector.connect(**db_config_student)
        cursor= connection.cursor()

        # Check if any field is empty
        if not self.purpose_entry.get() or not self.day_var.get() or not self.month_var.get() or not self.year_var.get() or not self.day_var_joining.get() or not self.month_var_joining.get() or not self.year_var_joining.get():
            messagebox.showerror("Error", "All fields must be filled.")
            return

        # try:

        # Get the CMS ID of the current user
        cms_id = config.current_user_id[0]

        # Insert outpass data into the database

        query = "INSERT INTO Outpass (LeavingDate, JoiningDate, Purpose, OStatus, CMS) VALUES (%s, %s, %s, 'Pending', %s)"
        
        # Format LeavingDate and JoiningDate as datetime objects
        leaving_date = datetime(int(self.year_var.get()), int(self.month_var.get()), int(self.day_var.get()))
        joining_date = datetime(int(self.year_var_joining.get()), int(self.month_var_joining.get()), int(self.day_var_joining.get()))
        
        values = (leaving_date, joining_date, self.purpose_entry.get(), cms_id)
        cursor.execute(query, values)
        connection.commit()

        messagebox.showinfo("Success", "Outpass submitted successfully!")

        # Reset form fields
        self.purpose_entry.delete(0, tk.END)
        self.day_var.set('')
        self.month_var.set('')
        self.year_var.set('')
        self.day_var_joining.set('')
        self.month_var_joining.set('')
        self.year_var_joining.set('')

        #new data has been inserted and thus treeview should be refreshed:
        #clear the tree view first and then rerun the select query
        self.outpass_tree.delete(*self.outpass_tree.get_children())

        #refetching data from db
        query = f"call get_outpass_data_through_cms({config.current_user_id[0]})"
        cursor.execute(query)
        results = cursor.fetchall()

        for result in results:
            self.outpass_tree.insert('', tk.END, values=result)

        # except mysql.connector.Error as err:
        #     messagebox.showerror("Error", f"Database Error: {err}")