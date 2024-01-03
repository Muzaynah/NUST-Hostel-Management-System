import tkinter as tk
from tkinter import Button, Label, StringVar, ttk, Entry
from tkinter import messagebox  # Added to handle message boxes
import mysql.connector
import config
from config import db_config
import config

class Settings(tk.Frame):
    def __init__(self, master):

        super().__init__(master, bg='white')
        self.master = master
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.user_type = ""

        self.new_password_var = StringVar()

        label = Label(self, text="Change Password:", bg = 'white', font=('Microsoft YaHei UI Light', 22))
        label.pack(pady=(200,0))

        # Password
        def on_enter_password(e):
            pw = self.password.get()
            if pw == 'New Password':
                self.password.delete(0, 'end')
                self.password.config(show='*')

        def on_leave_password(e):
            pw = self.password.get()
            if pw == '':
                self.password.insert(0, 'New Password')
                self.password.config(show='')

        self.password = Entry(self, width=25, fg='black', bg='#D3D3D3', border=0,  # Use the same dark blue color
                              font=('Microsoft YaHei UI Light', 14))
        self.password.insert(0, 'New Password')
        self.password.bind('<FocusIn>', on_enter_password)
        self.password.bind('<FocusOut>', on_leave_password)
        self.password.pack(padx=20, pady=(40,20))

        save_button = Button(self, text='Save', command=self.save_password,
                             font=('Microsoft YaHei UI Light', 14), bg='#014a81', fg='white', border=0, width=25, height=1)
        save_button.pack(pady=20)


    def save_password(self):
        new_password = self.password.get()

        if new_password == 'New Password':
            messagebox.showerror("Error", "Please enter a new password.")
            return

        # Query to change password
        if config.current_user_type == 'Student':
            query = f"UPDATE Student SET sPassword = '{new_password}' WHERE cms = {config.current_user_id[0]}"
        elif config.current_user_type == 'Manager':
            query = f"UPDATE Manager SET mPassword = '{new_password}' WHERE MID = {config.current_user_id[0]}"

        # Execute the query and commit the changes
        self.cursor.execute(query)
        self.connection.commit()

        print(f"New Password: {new_password}")

        messagebox.showinfo("Success", "Password changed successfully!")