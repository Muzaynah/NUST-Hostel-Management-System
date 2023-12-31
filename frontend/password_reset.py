import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import mysql.connector
import config
from config import db_config
from backend.emailing import sendEmail

class PasswordResetScreen(tk.Frame):
    def __init__(self, master, email, on_reset_success, on_back):
        super().__init__(master)
        self.master = master
        self.email = email
        self.on_reset_success = on_reset_success
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.user_type = ""

        self.master.title("Reset Password")

        if config.current_user_type == "Student":
            # get email id
            query = f"SELECT sEmail FROM Student WHERE cms = {config.current_user_id[0]}"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.email = result[0]
            
        if config.current_user_type == "Manager":
            query = f"SELECT mEmail FROM Student WHERE mid = {config.current_user_id[0]}"
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.email = result[0]

        # Email label
        email_label = tk.Label(self, text=f"Password Reset for {self.email[0]}", font=('Microsoft YaHei UI Light', 16))
        email_label.pack(pady=(200,20))

        send_otp_button = tk.Button(self, text='Send OTP', command=self.send_otp, width=20, bg='#014a81', fg='white', border=0,
                            font=('Microsoft YaHei UI Light', 14))
        send_otp_button.pack(pady=20)

        # Entry field for OTP
        self.otp_var = tk.StringVar()
        otp_entry = tk.Entry(self, textvariable=self.otp_var, show='', width=20, font=('Microsoft YaHei UI Light', 14))
        otp_entry.pack(pady=(0, 10))
        otp_entry.insert(0, 'Enter OTP')  # Placeholder text
        otp_entry.bind("<FocusIn>", self.on_entry_click)  # Bind the function to the entry field
        otp_entry.bind("<FocusOut>", self.on_focus_out)  # Bind the function to the entry field

        verify_otp_button = tk.Button(self, text='Verify OTP', width=20, command=self.submit_otp, bg='#014a81', fg='white', border=0,
                              font=('Microsoft YaHei UI Light', 14))
        verify_otp_button.pack(pady=20)

        self.otp_sent = False  # Flag to track whether OTP has been sent

        # Add a "Back" button
        back_button = tk.Button(self, text='Back', command=self.back_to_login, width=20, bg='#014a81', fg='white', border=0,
                                font=('Microsoft YaHei UI Light', 14))
        back_button.pack(pady=(80, 0))

    def back_to_login(self):
        # Invoke the callback function to go back to the login screen
        if self.on_back:
            self.on_back()

    def submit_otp(self):
        if not self.otp_sent:
            messagebox.showwarning("OTP not sent", "Please send OTP first.")
            return

        entered_otp = self.otp_var.get()

        # Assuming verify_otp is a function that checks if the entered OTP is correct
        if self.verify_otp(entered_otp):
            self.open_set_password_window()
        else:
            messagebox.showerror("Wrong OTP", "Incorrect OTP. Please try again.")

    def open_set_password_window(self):
        set_password_window = tk.Toplevel(self.master)
        SetPasswordScreen(set_password_window, self.on_reset_success)

    def send_otp(self):
        self.otp = sendEmail(self.email, "forgot password")
        messagebox.showinfo("OTP Sent", "An OTP has been sent to your email.")
        self.otp_sent = True  # Set the flag to indicate OTP has been sent

    def verify_otp(self, entered_otp):
        # Replace this with actual logic to verify the entered OTP
        # For now, let's consider it verified if it matches the dummy OTP (1234)
        return self.otp == entered_otp

    def on_reset_success(self):
        print('here')

    def on_entry_click(self, event):
        """function that gets called whenever entry is clicked"""
        if self.otp_var.get() == 'Enter OTP':
           self.otp_var.set('')
           self.otp_entry.config(fg='black')

    def on_focus_out(self, event):
        """function that gets called whenever entry is clicked"""
        if self.otp_var.get() == '':
            self.otp_var.set('Enter OTP')
            self.otp_entry.config(fg='grey')

class SetPasswordScreen(tk.Frame):
    def __init__(self, master, on_reset_success):
        super().__init__(master)
        self.master = master
        self.on_reset_success = on_reset_success
        self.master.title("Set New Password")

        # Set the window size
        self.master.geometry('400x300')
        # Center the window on the screen
        win_width = self.master.winfo_reqwidth()
        win_height = self.master.winfo_reqheight()
        pos_x = int((self.master.winfo_screenwidth() - win_width) / 2)-100
        pos_y = int((self.master.winfo_screenheight() - win_height) / 2)-100
        self.master.geometry(f'+{pos_x}+{pos_y}')

        # Connect to the database
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.password_entry = Entry(self.master, show='')

        # Configure the window appearance
        self.configure(bg='#014a81')  # Background color
        self.create_widgets()

    def create_widgets(self):
        label = Label(self.master, text="Enter your new password:", font=('Microsoft YaHei UI Light', 14), fg='black')
        label.pack(pady=(50,20))

        self.password_entry.pack(pady=20, ipadx=10, ipady=5)
        self.password_entry.insert(0, 'Enter Password')  # Placeholder text
        self.password_entry.bind("<FocusIn>", self.on_entry_click)  # Bind the function to the entry field
        self.password_entry.bind("<FocusOut>", self.on_focus_out)  # Bind the function to the entry field

        save_button = Button(self.master, text="Save", command=self.save_password, bg='#014a81', fg='white', border=0,
                             font=('Microsoft YaHei UI Light', 14))
        save_button.pack(pady=20)

    def save_password(self):
        new_password = self.password_entry.get()

        # Query to change password
        if config.current_user_type == 'Student':
            query = f"UPDATE Student SET sPassword = '{new_password}' WHERE cms = {config.current_user_id[0]}"
        elif config.current_user_type == 'Manager':
            query = f"UPDATE Manager SET mPassword = '{new_password}' WHERE MID = {config.current_user_id[0]}"

        # Execute the query and commit the changes
        self.cursor.execute(query)
        self.connection.commit()

        # Show success message
        messagebox.showinfo("Password Reset", "Your password has been changed successfully.")

        # Close the current window and invoke the callback function to go back to the login screen
        self.master.destroy()
        self.on_reset_success()

    def on_entry_click(self, event):
        """Function that gets called whenever entry is clicked"""
        if self.password_entry.get() == 'Enter Password':
            self.password_entry.delete(0, 'end')
            self.password_entry.config(show='*')  # Show '*' for password input
            self.password_entry.config(fg='black')

    def on_focus_out(self, event):
        """Function that gets called whenever entry is clicked"""
        if self.password_entry.get() == '':
            self.password_entry.insert(0, 'Enter Password')
            self.password_entry.config(show='')  # Hide text for placeholder
            self.password_entry.config(fg='grey')