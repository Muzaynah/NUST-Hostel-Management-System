# config.py
# This file contains the database configuration (db_config) dictionary
# Replace 'your_username', 'your_password', and 'your_database' with your actual MySQL credentials

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'ISR@m@nsoor0785',
    'database': 'project',
    'raise_on_warnings': True
}

# main.py
import tkinter as tk
from tkinter import Button, Entry, Label, Listbox, Scrollbar, StringVar, OptionMenu, messagebox, ttk
from datetime import datetime
import mysql.connector
from config import db_config

class StudentComplaint(tk.Frame):
    def __init__(self, master, show_dashboard):
        super().__init__(master)
        self.master = master
        self.show_dashboard = show_dashboard
        self.create_widgets()

    def create_widgets(self):
        # Create a frame for the left section (file complaints)
        left_frame = tk.Frame(self, width=600, height=600, bg='white')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for the right section (complaint history)
        right_frame = tk.Frame(self, width=600, height=600, bg='white')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        # File Complaint section (Left Frame)
        Label(left_frame, text='File a Complaint', font=('Helvetica', 16)).pack(pady=20)

        # Entry widgets for the complaint form
        complaint_label = Label(left_frame, text='Complaint:')
        complaint_label.pack()
        complaint_entry = Entry(left_frame)
        complaint_entry.pack()

        # Status label
        status_label = Label(left_frame, text='Status: Pending')
        status_label.pack()

        # Submit button
        submit_button = Button(left_frame, text='Submit', command=lambda: self.submit_complaint(complaint_entry.get()))
        submit_button.pack(pady=10)

        # Complaint History section (Right Frame)
        Label(right_frame, text='Complaint History', font=('Helvetica', 16)).pack(pady=20)

        # Treeview to display complaint history
        complaint_tree = ttk.Treeview(right_frame, columns=('Complaint', 'Status'), show='headings', height=15)
        complaint_tree.heading('Complaint', text='Complaint')
        complaint_tree.heading('Status', text='Status')
        complaint_tree.pack(pady=10)

        # Example data for the treeview (replace with actual data)
        complaint_data = [("Complaint 1", "In Progress"), ("Complaint 2", "Resolved"), ("Complaint 3", "Pending")]
        for item in complaint_data:
            complaint_tree.insert('', tk.END, values=item)

        # Scrollbar for the treeview
        scrollbar = Scrollbar(right_frame, orient=tk.VERTICAL, command=complaint_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        complaint_tree.config(yscrollcommand=scrollbar.set)

        # Back to dashboard button
        Button(self, text='Back to Dashboard', command=self.show_dashboard).pack(pady=20)

    def submit_complaint(self, complaint):
        # Check if the complaint field is empty
        if not complaint:
            messagebox.showerror("Error", "Complaint field must be filled.")
            return

        try:
            # Connect to the database
            connection = mysql.connector.connect(**db_config)
            cursor = connection.cursor()

            # Insert complaint data into the database
            query = "INSERT INTO Complaints (Complaint, Status) VALUES (%s, 'Pending')"
            values = (complaint,)
            cursor.execute(query, values)
            connection.commit()

            messagebox.showinfo("Success", "Complaint submitted successfully!")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Database Error: {err}")

        finally:
            # Close the database connection
            if connection.is_connected():
                cursor.close()
                connection.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentComplaint(root, show_dashboard=lambda: print("Back to Dashboard"))
    app.pack()
    root.mainloop()
