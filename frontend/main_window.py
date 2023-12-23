# main_window.py
import tkinter as tk
from frontend.login_page import LoginPage
from frontend.admin_screen import AdminScreen
from frontend.student_screen import StudentScreen

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('NUST Hostel Management System')
        self.geometry('1200x600+50+20')
        self.iconbitmap('assets/nust_logo.ico')

        # Create login page and student/admin pages
        self.login_page = LoginPage(self, self.show_admin_page, self.show_student_page)
        self.admin_screen = AdminScreen(self)
        self.student_screen = StudentScreen(self)

        # Set the login page as the initial page
        self.login_page.grid(row=0, column=0, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_admin_page(self):
        # Switch to the admin screen
        self.login_page.grid_forget()  # Remove the login page
        self.student_screen.grid_forget()  # Remove the student screen if it's showing
        self.admin_screen.grid(row=0, column=0, sticky='nsew')  # Show the admin screen

    def show_student_page(self):
        # Switch to the student screen
        self.login_page.grid_forget()  # Remove the login page
        self.admin_screen.grid_forget()  # Remove the admin screen if it's showing
        self.student_screen.grid(row=0, column=0, sticky='nsew')  # Show the student screen

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()