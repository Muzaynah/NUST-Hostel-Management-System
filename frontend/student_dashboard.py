#student_dashboard.py
import tkinter as tk
from tkinter import Label
from tkinter import Button

class StudentDashboard(tk.Frame):
    def __init__(self, master, show_outpass, show_complaints, show_attendance):
        super().__init__(master)
        self.master = master
        self.show_outpass = show_outpass
        self.show_complaints = show_complaints
        self.show_attendance = show_attendance
        self.create_widgets()

    def create_widgets(self):
        Label(self, text='Welcome to the Student Dashboard', font=('Helvetica', 16)).pack(pady=20)

        # Buttons for different sections
        Button(self, text='Outpass', command=self.show_outpass).pack(pady=10)
        Button(self, text='Complaints', command=self.show_complaints).pack(pady=10)
        Button(self, text='Attendance', command=self.show_attendance).pack(pady=10)