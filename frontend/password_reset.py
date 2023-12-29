import tkinter as tk
from tkinter import Label, Entry, Button, messagebox

class PasswordResetScreen(tk.Frame):
    def __init__(self, master, email, on_reset_success):
        super().__init__(master)
        self.master = master
        self.email = email
        self.on_reset_success = on_reset_success

        self.master.title("Reset Password")

        # Email label
        email_label = tk.Label(self, text=f"Password Reset for {self.email}", font=('Helvetica', 16))
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
        # Replace this with actual logic to generate and send an OTP to the user's email
        # For now, let's use a dummy OTP (1234)
        messagebox.showinfo("OTP Sent", "An OTP has been sent to your email.")
        self.otp_var.set("1234")  # Dummy OTP for testing

    def verify_otp(self, entered_otp):
        # Replace this with actual logic to verify the entered OTP
        # For now, let's consider it verified if it matches the dummy OTP (1234)
        return entered_otp == "1234"

class SetPasswordScreen(tk.Frame):
    def __init__(self, master, on_reset_success):
        super().__init__(master)
        self.master = master
        self.on_reset_success = on_reset_success

        self.master.title("Set New Password")

        self.label = Label(self, text="Enter your new password:")
        self.label.pack(pady=10)

        self.password_entry = Entry(self, show="*")
        self.password_entry.pack(pady=10)

        self.save_button = Button(self, text="Save", command=self.save_password)
        self.save_button.pack(pady=10)

    def save_password(self):
        new_password = self.password_entry.get()

        # Assuming save_password is a function that saves the new password
        # Replace this with your actual logic
        save_password(new_password)

        messagebox.showinfo("Password Reset", "Your password has been reset successfully.")

        self.master.destroy()  # Close the current window
        self.on_reset_success()  # Invoke the callback function to go back to the login screen

# Placeholder function for save_password (replace with actual logic)
def save_password(new_password):
    # Replace this with your actual logic to save the new password
    print(f"Saving password: {new_password}")
