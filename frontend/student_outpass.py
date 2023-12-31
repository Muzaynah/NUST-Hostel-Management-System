import tkinter as tk
from tkinter import Button, Entry, Label, Listbox, Scrollbar, StringVar, OptionMenu, messagebox
from datetime import datetime
import mysql.connector
from config import db_config_student
import config

class StudentOutpass(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the left section (apply for outpass)
        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the right section (outpass log)
        right_frame = tk.Frame(self, width=600, height=600, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Request an outpass section (Left Frame)
        Label(left_frame, text='Request an Outpass', font=('Helvetica', 16)).pack(pady=20)

        # Entry widgets for outpass request form
        purpose_label = Label(left_frame, text='Purpose:')
        purpose_label.pack()
        self.purpose_entry = Entry(left_frame)
        self.purpose_entry.pack()

        # Leaving Date
        leaving_date_label = Label(left_frame, text='Leaving Date:')
        leaving_date_label.pack()

        # Drop-down menus for day, month, and year
        self.day_var = StringVar()
        self.month_var = StringVar()
        self.year_var = StringVar()

        day_menu = OptionMenu(left_frame, self.day_var, *range(1, 32))
        month_menu = OptionMenu(left_frame, self.month_var, *range(1, 13))
        year_menu = OptionMenu(left_frame, self.year_var, *range(datetime.now().year, datetime.now().year + 1))

        day_menu.pack()
        month_menu.pack()
        year_menu.pack()

        # Joining Date
        joining_date_label = Label(left_frame, text='Joining Date:')
        joining_date_label.pack()

        # Drop-down menus for day, month, and year
        self.day_var_joining = StringVar()
        self.month_var_joining = StringVar()
        self.year_var_joining = StringVar()

        day_menu_joining = OptionMenu(left_frame, self.day_var_joining, *range(1, 32))
        month_menu_joining = OptionMenu(left_frame, self.month_var_joining, *range(1, 13))
        year_menu_joining = OptionMenu(left_frame, self.year_var_joining, *range(datetime.now().year, datetime.now().year + 1))

        day_menu_joining.pack()
        month_menu_joining.pack()
        year_menu_joining.pack()

        # Submit button
        submit_button = Button(left_frame, text='Submit', command=self.submit_outpass)
        submit_button.pack(pady=10)

        # Outpass Log section (Right Frame)
        Label(right_frame, text='Outpass Requests and History', font=('Helvetica', 16)).pack(pady=20)

        # Listbox to display outpass requests and history
        outpass_listbox = Listbox(right_frame, selectmode=tk.SINGLE, width=40, height=15)
        outpass_listbox.pack(pady=10)

        # Example data for the listbox (replace with actual data)
        outpass_data = ["Request 1 - Pending", "Request 2 - Approved", "Request 3 - Rejected"]
        for item in outpass_data:
            outpass_listbox.insert(tk.END, item)

        # Scrollbar for the listbox
        scrollbar = Scrollbar(right_frame, orient=tk.VERTICAL)
        scrollbar.config(command=outpass_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        outpass_listbox.config(yscrollcommand=scrollbar.set)

    def submit_outpass(self):
        # Check if any field is empty
        if not self.purpose_entry.get() or not self.day_var.get() or not self.month_var.get() or not self.year_var.get() or not self.day_var_joining.get() or not self.month_var_joining.get() or not self.year_var_joining.get():
            messagebox.showerror("Error", "All fields must be filled.")
            return

        try:
            # Connect to the database
            connection = mysql.connector.connect(**db_config_student)
            cursor = connection.cursor()

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
            self.year_var_joining.set()

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()