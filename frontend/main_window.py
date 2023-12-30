import tkinter as tk
from tkinter import Button
from frontend.login_page import LoginPage
from frontend.admin_dashboard import AdminDashboard
from frontend.student_dashboard import StudentDashboard
from frontend.student_outpass import StudentOutpass
from frontend.student_complaint import StudentComplaint
from frontend.student_attendance import StudentAttendance
from frontend.admin_attendance import AdminAttendance
from frontend.admin_student import AdminStudent, AddStudentWindow
from frontend.password_reset import PasswordResetScreen
from frontend.admin_complaint import AdminComplaint
from frontend.admin_outpass import AdminOutpass
from frontend.admin_notification import AdminNotification
import config  # Import config where it's needed

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('NUST Hostel Management System')

        # Set the window state to 'zoomed' for fullscreen
        self.wm_state('zoomed')
        self.iconbitmap('assets/nust_logo.ico')

        # Create login page and student/admin pages
        #self.login_page = LoginPage(self, self.show_admin_dashboard, self.show_student_dashboard) #,self.current_user_id
        # self.admin_dashboard = AdminDashboard(self, self.show_moutpass, self.show_mcomplaint, self.show_mattendance, self.show_mhostel, self.show_mstudent, self.show_mnotification)
        # self.student_dashboard = StudentDashboard(self, self.show_outpass, self.show_complaints, self.show_attendance)
        self.login_page = LoginPage(self, self.show_admin_dashboard, self.show_student_dashboard, self.show_password_reset)
        self.password_reset=None

        # student - none ---------------------
        self.student_dashboard = None
        self.student_outpass = None
        self.student_attendance = None
        self.student_complaint = None

        # admin - none -----------------------
        self.admin_dashboard = None
        self.admin_outpass = None
        self.admin_attendance = None
        self.admin_complaint = None
        self.admin_student = None
        self.admin_notification = None

        # global current_user_id
        # self.current_user_id = current_user_id

        #side panel for student ----------------------------------------

        # Create a frame for the side panel
        self.student_side_panel = tk.Frame(self, bg='#1a2530', width=200)
        
        # Add buttons to the side panel 
        Button(self.student_side_panel, text='Edit Profile', command=self.show_edit_profile, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=2, pady=(8,3))
        Button(self.student_side_panel, text='Student Dashboard', command=self.show_student_dashboard, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=3)
        Button(self.student_side_panel, text='Contact Admin', command=self.show_contact_admin, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=3)
        Button(self.student_side_panel, text='Settings', command=self.show_settings, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=3)
        Button(self.student_side_panel, text='Log Out', command=self.show_login_page, bg='#014a81', fg='white', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=(3, 50), side=tk.BOTTOM, anchor=tk.S)

        #side panel for admin ----------------------------------------

        # Create a frame for the side panel
        self.admin_side_panel = tk.Frame(self, bg='#1a2530', width=200)
        
        # Add buttons to the side panel 
        Button(self.admin_side_panel, text='Edit Profile', command=self.show_edit_profile, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=2, pady=(8,3))
        Button(self.admin_side_panel, text='Admin Dashboard', command=self.show_admin_dashboard, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=3)
        Button(self.admin_side_panel, text='Manage Students', command=self.show_contact_admin, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=3)
        Button(self.admin_side_panel, text='Settings', command=self.show_settings, bg='white', fg='black', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=3)
        Button(self.admin_side_panel, text='Log Out', command=self.show_login_page, bg='#014a81', fg='white', border=0, width=25, height=2, font=('Helvetica', 10)).pack(padx=6,pady=(3, 50), side=tk.BOTTOM, anchor=tk.S)

        # Set the login page as the initial page
        self.show_login_page()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # Make the side panel fixed in width

        # Initially hide the side panels
        self.admin_side_panel.grid_forget()
        self.student_side_panel.grid_forget()

    def create_student_dashboard(self):
        # Create the student dashboard dynamically
        self.student_dashboard = StudentDashboard(self, self.show_outpass, self.show_complaints, self.show_attendance)
        self.student_outpass = StudentOutpass(self, self.show_student_dashboard)
        self.student_attendance = StudentAttendance(self,self.show_student_dashboard)
        self.student_complaint = StudentComplaint(self,self.show_student_dashboard)

    def create_admin_dashboard(self):
        # Create the student dashboard dynamically
        self.admin_dashboard = AdminDashboard(self, self.show_moutpass, self.show_mcomplaint, self.show_mattendance, self.show_mstudent, self.show_mnotification)
        self.admin_student = AdminStudent(self, self.show_admin_dashboard)
        self.admin_attendance = AdminAttendance(self)
        self.admin_complaint = AdminComplaint(self)
        self.admin_outpass = AdminOutpass(self)
        self.admin_notification = AdminNotification(self, self.show_add_student)

    def show_admin_dashboard(self):
        # Switch to the admin screen
        self.login_page.grid_forget()  # Remove the login page
        if self.student_dashboard is not None:
            self.student_dashboard.grid_forget()  # Remove the student dashboard if it's showing
        if self.student_outpass is not None:
            self.student_outpass.grid_forget()  # Remove the student outpass if it's showing
        if self.student_attendance is not None:
            self.student_attendance.grid_forget()  # Remove the student attendance if it's showing
        if self.student_complaint is not None:
            self.student_complaint.grid_forget()  # Remove the student complaint if it's showing
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        if self.admin_dashboard is None:
            print('creating admin dashboard')
            self.create_admin_dashboard()

        self.admin_dashboard.grid(row=0, column=0, sticky='nsew')  # Show the admin screen
        self.student_side_panel.grid_forget()  # Hide the student side panel
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')  # Show the admin side panel

    def show_student_dashboard(self):
        print(config.current_user_id)
        # Your existing code for show_student_dashboard goes here):
        # Switch to the student dashboard
        self.login_page.grid_forget()  # Remove the login page
        if(self.admin_dashboard is not None):
            self.admin_dashboard.grid_forget()  # Remove the admin screen if it's showing
        if(self.student_outpass is not None):
            self.student_outpass.grid_forget() # Remove the outpass screen if it is showing
        if(self.student_attendance is not None):
            self.student_attendance.grid_forget()
        if(self.student_complaint is not None):
            self.student_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget() 

        if self.student_dashboard is None:
            print('creating student dashboard')
            self.create_student_dashboard()

        self.student_dashboard.grid(row=0, column=0, sticky='nsew')  # Show the student dashboard
        self.student_side_panel.grid(row=0, column=1, sticky='ns')  # Show the side panel
        self.admin_side_panel.grid_forget()  # Hide the student side panel
    
    # student buttons screens functions -------------------------------
    
    def show_edit_profile(self):
        # Your code to switch to the edit profile section goes here
        print("Switching to Edit Profile Section")
        self.student_side_panel.grid(row=0, column=1, sticky='ns')

    def show_contact_admin(self):
        # Your code to switch to the contact admin section goes here
        print("Switching to Contact Admin Section")

    def show_settings(self):
        # Your code to switch to the settings section goes here
        print("Switching to Settings Section")
        self.student_side_panel.grid(row=0, column=1, sticky='ns')

    def show_login_page(self):
        # Switch to the login page
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.student_dashboard is not None:
            self.student_dashboard.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
            
        self.login_page.grid(row=0, column=0, sticky='nsew')  # Show the login page
        self.student_side_panel.grid_forget()
        self.admin_side_panel.grid_forget()

    def show_password_reset(self):
        # Call the PasswordResetScreen with the current user's email and a callback to show the login page
        email = "user@example.com"  # You need to implement a function to get the current user's email
        if self.login_page is not None:
            self.login_page.grid_forget()
        self.password_reset = PasswordResetScreen(self, email, self.show_login_page)
        self.password_reset.grid(row=0, column=0, sticky='nsew')
        
    def show_complaints(self):
        # Your code to switch to the complaints section goes here
        print("Switching to Complaints Section")
        if(self.student_dashboard is not None):
            self.student_dashboard.grid_forget()  # Remove the student dashboard if it's showing
        if(self.student_outpass is not None):
            self.student_outpass.grid_forget()
        if(self.student_attendance is not None):
            self.student_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.student_complaint.grid(row=0, column=0, sticky='nsew')  
        self.student_side_panel.grid(row=0, column=1, sticky='ns')  # Show the side panel

    def show_attendance(self):
        # Your code to switch to the attendance section goes here
        print("Switching to Attendance Section")
        if(self.student_dashboard is not None):
            self.student_dashboard.grid_forget()  # Remove the student dashboard if it's showing
        if(self.student_complaint is not None):
            self.student_complaint.grid_forget()
        if(self.student_outpass is not None):
            self.student_outpass.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        
        self.student_attendance.grid(row=0, column=0, sticky='nsew')
        self.student_side_panel.grid(row=0, column=1, sticky='ns')  # Show the side panel

    def show_outpass(self):
        # Switch to the student outpass screen
        print("Switching to Outpass Section")
        if(self.student_dashboard is not None):
            self.student_dashboard.grid_forget()  # Remove the student dashboard if it's showing
        if(self.student_complaint is not None):
            self.student_complaint.grid_forget()
        if(self.student_attendance is not None):
            self.student_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.student_outpass.grid(row=0, column=0, sticky='nsew')  # Show the student outpass screen
        self.student_side_panel.grid(row=0, column=1, sticky='ns')  # Show the side panel

    
    # admin buttons screens functions ------------------------------

    def show_mstudent(self):
        # Your code to switch to the complaints section goes here
        print("Switching to student Section") 
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if(self.admin_dashboard is not None):
            self.admin_dashboard.grid_forget()
        if(self.admin_outpass is not None):
            self.admin_outpass.grid_forget()
        if(self.admin_attendance is not None):
            self.admin_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()

        self.admin_student.grid(row=0, column=0, sticky='nsew')  

    def show_add_student(self):
        # Show the add student window
        print("Adding student:")
        self.add_student_window = AddStudentWindow(self, self.add_student)

    def add_student(self, student_data):
        # Handle adding a new student to the database (you need to implement this part)
        # For now, print the student data
        print("Adding student:", student_data)
        # Update the student table
        self.admin_student.update_student_table([list(student_data.values())])

    def show_mnotification(self):
        # Your code to switch to the attendance section goes here
        print("Switching to admin notification Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if(self.admin_dashboard is not None):
            self.admin_dashboard.grid_forget()
        if(self.admin_outpass is not None):
            self.admin_outpass.grid_forget()
        if(self.student_complaint is not None):
            self.admin_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_notification.grid(row=0, column=0, sticky='nsew')

    def show_mcomplaint(self):
        # Your code to switch to the complaints section goes here
        print("Switching to admin Complaints Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if(self.admin_dashboard is not None):
            self.admin_dashboard.grid_forget()
        if(self.admin_outpass is not None):
            self.admin_outpass.grid_forget()
        if(self.student_attendance is not None):
            self.admin_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_complaint.grid(row=0, column=0, sticky='nsew') 

    def show_mattendance(self):
        # Your code to switch to the attendance section goes here
        print("Switching to admin Attendance Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if(self.admin_dashboard is not None):
            self.admin_dashboard.grid_forget()
        if(self.admin_outpass is not None):
            self.admin_outpass.grid_forget()
        if(self.student_complaint is not None):
            self.admin_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_attendance.grid(row=0, column=0, sticky='nsew')

    def show_moutpass(self):
        # Switch to the student outpass screen
        print("Switching to admin Outpass Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if(self.admin_dashboard is not None):
            self.admin_dashboard.grid_forget()
        if(self.admin_complaint is not None):
            self.admin_complaint.grid_forget()
        if(self.admin_attendance is not None):
            self.admin_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_outpass.grid(row=0, column=0, sticky='nsew')  # Show the outpass screen


if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()