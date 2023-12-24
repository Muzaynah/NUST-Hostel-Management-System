import tkinter as tk
from tkinter import Button
from frontend.login_page import LoginPage
from frontend.admin_screen import AdminScreen
from frontend.student_dashboard import StudentDashboard
from frontend.student_outpass import StudentOutpass

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('NUST Hostel Management System')
        # Set the window state to 'zoomed' for fullscreen
        self.wm_state('zoomed')
        self.iconbitmap('assets/nust_logo.ico')

        # Create login page and student/admin pages
        self.login_page = LoginPage(self, self.show_admin_page, self.show_student_dashboard)
        self.admin_screen = AdminScreen(self)
        self.student_dashboard = StudentDashboard(self, self.show_outpass, self.show_complaints, self.show_attendance)
        self.student_outpass = StudentOutpass(self, self.show_student_dashboard)

        # Create a frame for the side panel
        self.side_panel = tk.Frame(self, bg='#F6f6f6', width=200)

        # Initially hide the side panel
        self.side_panel.grid_forget()

        # Add buttons to the side panel 
        Button(self.side_panel, text='Edit Profile', command=self.show_edit_profile, bg='white', fg='black', width=25, height=2, font=('Helvetica', 10)).pack(pady=(20,0))
        Button(self.side_panel, text='Student Dashboard', command=self.show_student_dashboard, bg='white', fg='black', width=25, height=2, font=('Helvetica', 10)).pack(pady=0)
        Button(self.side_panel, text='Contact Admin', command=self.show_contact_admin, bg='white', fg='black', width=25, height=2, font=('Helvetica', 10)).pack(pady=0)
        Button(self.side_panel, text='Settings', command=self.show_settings, bg='white', fg='black', width=25, height=2, font=('Helvetica', 10)).pack(pady=0)
        Button(self.side_panel, text='Log Out', command=self.show_login_page, bg='#014a81', fg='white', width=25, height=2, font=('Helvetica', 10)).pack(pady=(0, 50), side=tk.BOTTOM, anchor=tk.S)

        # Set the login page as the initial page
        self.show_login_page()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # Make the side panel fixed in width

    def show_admin_page(self):
        # Switch to the admin screen
        self.login_page.grid_forget()  # Remove the login page
        self.student_dashboard.grid_forget()  # Remove the student dashboard if it's showing
        self.admin_screen.grid(row=0, column=0, sticky='nsew')  # Show the admin screen
        self.side_panel.grid_forget()  # Hide the side panel

    def show_student_dashboard(self):
        # Switch to the student dashboard
        self.login_page.grid_forget()  # Remove the login page
        self.admin_screen.grid_forget()  # Remove the admin screen if it's showing
        self.student_outpass.grid_forget() # Remove the outpass screen if it is showing
        self.student_dashboard.grid(row=0, column=0, sticky='nsew')  # Show the student dashboard
        self.side_panel.grid(row=0, column=1, sticky='ns')  # Show the side panel

    def show_edit_profile(self):
        # Your code to switch to the edit profile section goes here
        print("Switching to Edit Profile Section")

    def show_contact_admin(self):
        # Your code to switch to the contact admin section goes here
        print("Switching to Contact Admin Section")

    def show_settings(self):
        # Your code to switch to the settings section goes here
        print("Switching to Settings Section")

    def show_login_page(self):
        # Switch to the login page
        self.admin_screen.grid_forget()  # Remove the admin screen if it's showing
        self.student_dashboard.grid_forget()  # Remove the student dashboard if it's showing
        self.login_page.grid(row=0, column=0, sticky='nsew')  # Show the login page
        self.side_panel.grid_forget()  # Hide the side panel

    # Functions to handle transitions to specific sections/screens
    def show_complaints(self):
        # Your code to switch to the complaints section goes here
        print("Switching to Complaints Section")

    def show_attendance(self):
        # Your code to switch to the attendance section goes here
        print("Switching to Attendance Section")

    def show_outpass(self):
        # Switch to the student outpass screen
        print("Switching to Outpass Section")
        self.student_dashboard.grid_forget()  # Remove the student dashboard if it's showing
        self.student_outpass.grid(row=0, column=0, sticky='nsew')  # Show the student outpass screen
        self.side_panel.grid(row=0, column=1, sticky='ns')  # Show the side panel

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()