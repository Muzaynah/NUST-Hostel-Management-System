# main_window.py
import tkinter as tk
from frontend.login_page import LoginPage
from frontend.admin_screen import AdminScreen
from frontend.student_dashboard import StudentDashboard
from frontend.student_outpass import StudentOutpass

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('NUST Hostel Management System')
        self.geometry('1200x600+50+20')
        self.iconbitmap('assets/nust_logo.ico')

        # Create login page and student/admin pages
        self.login_page = LoginPage(self, self.show_admin_page, self.show_student_dashboard)
        self.admin_screen = AdminScreen(self)
        self.student_dashboard = StudentDashboard(self, self.show_outpass, self.show_complaints, self.show_attendance)
        self.student_outpass = StudentOutpass(self, self.show_student_dashboard)

        # Set the login page as the initial page
        self.login_page.grid(row=0, column=0, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_admin_page(self):
        # Switch to the admin screen
        self.login_page.grid_forget()  # Remove the login page
        self.student_screen.grid_forget()  # Remove the student screen if it's showing
        self.admin_screen.grid(row=0, column=0, sticky='nsew')  # Show the admin screen

    def show_student_dashboard(self):
        # Switch to the student dashboard
        self.login_page.grid_forget()  # Remove the login page
        self.admin_screen.grid_forget()  # Remove the admin screen if it's showing
        self.student_outpass.grid_forget() # Remove the outpass screen if it is showing
        self.student_dashboard.grid(row=0, column=0, sticky='nsew')  # Show the student dashboard

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


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()