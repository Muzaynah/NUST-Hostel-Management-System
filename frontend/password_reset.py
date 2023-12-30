import tkinter as tk
from tkinter import Label, Entry, Button, messagebox
import mysql.connector
import config
from config import db_config
from backend.emailing import sendEmail

class PasswordResetScreen(tk.Frame):
    def __init__(self, master, email, on_reset_success):
        super().__init__(master)
        self.master = master
        self.email = email
        self.on_reset_success = on_reset_success
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.user_type = ""

        self.master.title("Reset Password")

        if(config.current_user_type=="Student"):
            #get email id
            query = f"SELECT sEmail FROM Student WHERE cms = {config.current_user_id[0]}"
            self.cursor.execute(query)
            result=self.cursor.fetchall()
            self.email = result[0]
            # print(self.email)
            
        if(config.current_user_type=="Manager"):
            query=f"SELECT mEmail FROM Student WHERE mid = {config.current_user_id[0]}"
            self.cursor.execute(query)
            result=self.cursor.fetchall()
            self.email = result[0]
            # print(self.email)

        # Email label
        email_label = tk.Label(self, text=f"Password Reset for {self.email[0]}", font=('Helvetica', 16))
        email_label.pack(pady=20)

        # Add the label properly
        label_instruction = Label(self, text="Please enter the OTP sent to your email address")
        label_instruction.pack()

        send_otp_button = tk.Button(self, text='Send OTP', command=self.send_otp)
        send_otp_button.pack(pady=10)

        # OTP entry and verification
        self.otp_var = tk.StringVar()
        otp_label = tk.Label(self, text='Enter OTP:')
        otp_label.pack(pady=(0, 5))
        otp_entry = tk.Entry(self, textvariable=self.otp_var, show='*')
        otp_entry.pack(pady=(0, 10))

        verify_otp_button = tk.Button(self, text='Verify OTP', command=self.submit_otp)
        verify_otp_button.pack(pady=10)

    def submit_otp(self):
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
        self.otp = sendEmail(self.email,"forgot password")
        messagebox.showinfo("OTP Sent", "An OTP has been sent to your email.")
        # self.otp_var.set("1234")  # Dummy OTP for testing

    def verify_otp(self, entered_otp):
        # Replace this with actual logic to verify the entered OTP
        # For now, let's consider it verified if it matches the dummy OTP (1234)
        return self.otp == entered_otp
    
    def on_reset_success(self):
        print('here')

class SetPasswordScreen(tk.Frame):
    def __init__(self, master, on_reset_success):
        super().__init__(master)
        self.master = master
        self.on_reset_success = on_reset_success
        self.master.title("Set New Password")
        self.master.geometry('300x300')
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()
        self.password_entry = Entry(self.master, show="*")
    
        self.create_widgets()

    def create_widgets(self):
        # testlabel = Label(self.master, width=20, height=20, bg="#FF0000")
        # testlabel.pack()

        label = Label(self.master, text="Enter your new password:")
        label.pack(pady=10)

        self.password_entry.pack(pady=10)

        save_button = Button(self.master, text="Save", command=self.save_password)
        save_button.pack(pady=10)

    def save_password(self):
        new_password = self.password_entry.get()

        #query to change password
        if(config.current_user_type=='Student'):
            query = f"UPDATE Student SET sPassword = '{new_password}' WHERE cms = {config.current_user_id[0]}"
        elif(config.current_user_type=='Manager'):
            query = f"UPDATE Manager SET mPassword = '{new_password}' WHERE MID = {config.current_user_id[0]}"
        self.cursor.execute(query)
        self.connection.commit()
        
        messagebox.showinfo("Password Reset", "Your password has been changed successfully.")

        self.master.destroy()  # Close the current window
        self.on_reset_success()  # Invoke the callback function to go back to the login screen