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
from frontend.settings import Settings
import config  

#1f2b38 dark
#E0E6EE bg light
#014a81 nust blue
#2270ab lighter nust blue

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('NUST Hostel Management System')
        self.wm_state('zoomed')  # Set the window state to 'zoomed' for fullscreen
        self.iconbitmap('assets/nust_logo.ico')

        # Create login page and student/admin pages
        self.login_page = LoginPage(self, self.show_admin_dashboard, self.show_student_dashboard, self.show_password_reset)
        self.password_reset = None
        self.settings = None

        # student - none
        self.student_dashboard = None
        self.student_outpass = None
        self.student_attendance = None
        self.student_complaint = None

        # admin - none
        self.admin_dashboard = None
        self.admin_outpass = None
        self.admin_attendance = None
        self.admin_complaint = None
        self.admin_student = None
        self.admin_notification = None

        # side panel for student
        self.student_side_panel = tk.Frame(self, bg='#171d22', width=200)
        Button(self.student_side_panel, text='Student Dashboard', command=self.show_student_dashboard, bg='#2270ab', fg='white', border=0, width=18, height=1, font=('Microsoft YaHei UI Light', 14)).pack(padx=6, pady=(35, 4))
        Button(self.student_side_panel, text='Settings', command=self.show_settings, bg='#C5e2f8', fg='black', border=0, width=20, height=1, font=('Microsoft YaHei UI Light', 12, 'bold')).pack(padx=6, pady=(4, 20), side=tk.BOTTOM, anchor=tk.S)
        Button(self.student_side_panel, text='Log Out', command=self.show_login_page, bg='#C5e2f8', fg='black', border=0, width=20, height=1, font=('Microsoft YaHei UI Light', 12, 'bold')).pack(padx=6, pady=4, side=tk.BOTTOM, anchor=tk.S)

        # side panel for admin
        self.admin_side_panel = tk.Frame(self, bg='#171d22', width=200)
        Button(self.admin_side_panel, text='Admin Dashboard', command=self.show_admin_dashboard, bg='#2270ab', fg='white', border=0, width=18, height=1, font=('Microsoft YaHei UI Light', 14)).pack(padx=6, pady=(35, 4))
        Button(self.admin_side_panel, text='Settings', command=self.show_settings, bg='#C5e2f8', fg='black', border=0, width=20, height=1, font=('Microsoft YaHei UI Light', 12, 'bold')).pack(padx=6, pady=(4, 20), side=tk.BOTTOM, anchor=tk.S)
        Button(self.admin_side_panel, text='Log Out', command=self.show_login_page, bg='#C5e2f8', fg='black', border=0, width=20, height=1, font=('Microsoft YaHei UI Light', 12, 'bold')).pack(padx=6, pady=4, side=tk.BOTTOM, anchor=tk.S)

        # Set the login page as the initial page
        self.show_login_page()
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)  # Make the side panel fixed in width

        # Initially hide the side panels
        self.admin_side_panel.grid_forget()
        self.student_side_panel.grid_forget()

    def create_student_dashboard(self):
        self.student_dashboard = StudentDashboard(self, self.show_outpass, self.show_complaints, self.show_attendance)
        self.student_outpass = StudentOutpass(self)
        self.student_attendance = StudentAttendance(self)
        self.student_complaint = StudentComplaint(self)

    def create_admin_dashboard(self):
        self.admin_dashboard = AdminDashboard(self, self.show_moutpass, self.show_mcomplaint, self.show_mattendance, self.show_mstudent, self.show_mnotification)
        self.admin_student = AdminStudent(self)
        self.admin_attendance = AdminAttendance(self)
        self.admin_complaint = AdminComplaint(self)
        self.admin_outpass = AdminOutpass(self)
        self.admin_notification = AdminNotification(self)

    def show_admin_dashboard(self):
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.admin_outpass is not None:
            self.admin_outpass.grid_forget()
        if self.admin_attendance is not None:
            self.admin_attendance.grid_forget()
        if self.admin_complaint is not None:
            self.admin_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        if self.admin_student is not None:
            self.admin_student.grid_forget()
        if self.admin_notification is not None:
            self.admin_notification.grid_forget()
        if self.settings is not None:
            self.settings.grid_forget()

        # Create or show the AdminDashboard
        if self.admin_dashboard is None:
            self.create_admin_dashboard()

        self.admin_dashboard.grid(row=0, column=0, sticky='nsew')
        self.student_side_panel.grid_forget()
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')

    def show_student_dashboard(self):
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.student_outpass is not None:
            self.student_outpass.destroy()
            self.student_outpass=None
            # self.student_outpass.grid_forget()
        if self.student_attendance is not None:
            self.student_attendance.destroy()
            self.student_attendance=None
            # self.student_attendance.grid_forget()
        if self.student_complaint is not None:
            self.student_complaint.destroy()
            self.student_complaint=None
            # self.student_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        if self.settings is not None:
            self.settings.grid_forget()
        if self.student_dashboard is None:
            self.create_student_dashboard()


        self.login_page.grid_forget()
        self.student_dashboard.grid(row=0, column=0, sticky='nsew')
        self.student_side_panel.grid(row=0, column=1, sticky='ns')
        self.admin_side_panel.grid_forget()

    def show_login_page(self):
        if self.admin_dashboard is not None:
            self.admin_dashboard.destroy()
            self.admin_dashboard = None
        if self.student_dashboard is not None:
            self.student_dashboard.destroy()
            self.student_dashboard = None
        if self.student_outpass is not None:
            self.student_outpass.destroy()
            self.student_outpass = None
        if self.student_attendance is not None:
            self.student_attendance.destroy()
            self.student_attendance = None
        if self.student_complaint is not None:
            self.student_complaint.destroy()
            self.student_complaint = None
        if self.password_reset is not None:
            self.password_reset.destroy()
            self.password_reset = None
        if self.admin_outpass is not None:
            self.admin_outpass.destroy()
            self.admin_outpass = None
        if self.admin_attendance is not None:
            self.admin_attendance.destroy()
            self.admin_attendance = None
        if self.admin_complaint is not None:
            self.admin_complaint.destroy()
            self.admin_complaint = None
        if self.admin_student is not None:
            self.admin_student.destroy()
            self.admin_student = None
        if self.admin_notification is not None:
            self.admin_notification.destroy()
            self.admin_notification = None
        if self.settings is not None:
            self.settings.grid_forget()

        self.student_side_panel.grid_forget()
        self.admin_side_panel.grid_forget()

        self.login_page.grid(row=0, column=0, sticky='nsew')  # Show the login page

    def show_settings(self):
        # Your code to switch to the settings section goes here
        print("Switching to Settings Section")

        # Forget all other screens
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.student_dashboard is not None:
            self.student_dashboard.grid_forget()
        if self.student_outpass is not None:
            self.student_outpass.grid_forget()
        if self.student_attendance is not None:
            self.student_attendance.grid_forget()
        if self.student_complaint is not None:
            self.student_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        if self.admin_outpass is not None:
            self.admin_outpass.grid_forget()
        if self.admin_attendance is not None:
            self.admin_attendance.grid_forget()
        if self.admin_complaint is not None:
            self.admin_complaint.grid_forget()
        if self.admin_student is not None:
            self.admin_student.grid_forget()
        if self.admin_notification is not None:
            self.admin_notification.grid_forget()

        self.settings = Settings(self)
        self.settings.grid(row=0, column=0, sticky='nsew')

        # Show the appropriate side panel
        if config.current_user_type == 'student':
            self.student_side_panel.grid(row=0, column=1, sticky='ns')
        elif config.current_user_type == 'admin':
            self.admin_side_panel.grid(row=0, column=1, sticky='ns')

    def show_password_reset(self):
        email = "user@example.com"
        if self.login_page is not None:
            self.login_page.grid_forget()
        self.password_reset = PasswordResetScreen(self, email, self.show_login_page, self.show_login_page)
        self.password_reset.grid(row=0, column=0, sticky='nsew')

    def show_complaints(self):
        print("Switching to Complaints Section")
        if self.student_complaint is None:
            self.student_complaint = StudentComplaint(self)
        if self.student_dashboard is not None:
            self.student_dashboard.grid_forget()
        if self.student_outpass is not None:
            self.student_outpass.grid_forget()
        if self.student_attendance is not None:
            self.student_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.student_complaint.grid(row=0, column=0, sticky='nsew')
        self.student_side_panel.grid(row=0, column=1, sticky='ns')

    def show_attendance(self):
        print("Switching to Attendance Section")
        if self.student_attendance is None:
            self.student_attendance = StudentAttendance(self)
        if self.student_dashboard is not None:
            self.student_dashboard.grid_forget()
        if self.student_complaint is not None:
            self.student_complaint.grid_forget()
        if self.student_outpass is not None:
            self.student_outpass.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()

        self.student_attendance.grid(row=0, column=0, sticky='nsew')
        self.student_side_panel.grid(row=0, column=1, sticky='ns')

    def show_outpass(self):
        print("Switching to Outpass Section")
        if self.student_outpass is None:
            self.student_outpass = StudentOutpass(self)
        if self.student_dashboard is not None:
            self.student_dashboard.grid_forget()
        if self.student_complaint is not None:
            self.student_complaint.grid_forget()
        if self.student_attendance is not None:
            self.student_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.student_outpass.grid(row=0, column=0, sticky='nsew')
        self.student_side_panel.grid(row=0, column=1, sticky='ns')

    def show_mstudent(self):
        print("Switching to student Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.admin_outpass is not None:
            self.admin_outpass.grid_forget()
        if self.admin_attendance is not None:
            self.admin_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()

        self.admin_student.grid(row=0, column=0, sticky='nsew')

    # def show_add_student(self):
    #     print("Adding student:")
    #     self.add_student_window = AddStudentWindow(self, self.add_student)

    # def add_student(self, student_data):
    #     print("Adding student:", student_data)
    #     self.admin_student.update_student_table([list(student_data.values())])

    def show_mnotification(self):
        print("Switching to admin notification Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.admin_outpass is not None:
            self.admin_outpass.grid_forget()
        if self.admin_complaint is not None:
            self.admin_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_notification.grid(row=0, column=0, sticky='nsew')

    def show_mcomplaint(self):
        print("Switching to admin Complaints Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.admin_outpass is not None:
            self.admin_outpass.grid_forget()
        if self.admin_attendance is not None:
            self.admin_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_complaint.grid(row=0, column=0, sticky='nsew')

    def show_mattendance(self):
        print("Switching to admin Attendance Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.admin_outpass is not None:
            self.admin_outpass.grid_forget()
        if self.admin_complaint is not None:
            self.admin_complaint.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_attendance.grid(row=0, column=0, sticky='nsew')

    def show_moutpass(self):
        print("Switching to admin Outpass Section")
        self.admin_side_panel.grid(row=0, column=1, sticky='ns')
        if self.admin_dashboard is not None:
            self.admin_dashboard.grid_forget()
        if self.admin_complaint is not None:
            self.admin_complaint.grid_forget()
        if self.admin_attendance is not None:
            self.admin_attendance.grid_forget()
        if self.password_reset is not None:
            self.password_reset.grid_forget()
        self.admin_outpass.grid(row=0, column=0, sticky='nsew')