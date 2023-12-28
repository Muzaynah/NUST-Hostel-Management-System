import tkinter as tk
from tkinter import ttk, Entry, Button, Toplevel, StringVar, Radiobutton, Scrollbar, LEFT, RIGHT, Y
import random

class AdminAttendance(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='white')
        self.master = master
        self.current_date_index = 0
        self.dates = ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04']
        self.attendance_data = {}
        self.create_widgets()

    def create_widgets(self):
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')

        self.date_var = StringVar()
        date_label = ttk.Label(center_frame, textvariable=self.date_var, font=('Helvetica', 12), style='Header.TLabel')
        date_label.pack(pady=(20, 10))

        columns = ('Student Name', 'Status')
        self.attendance_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        for col in columns:
            self.attendance_tree.heading(col, text=col)

        self.attendance_tree.column('Student Name', width=200)
        self.attendance_tree.column('Status', width=100)

        self.attendance_tree.pack(padx=20, pady=(0, 20), side=tk.TOP, fill=tk.BOTH, expand=True)

        left_button = Button(center_frame, text='<', command=self.show_previous_date, bg='#1a2530', fg='white', border=0,
                             width=2, height=1, font=('Helvetica', 12))
        left_button.pack(side=tk.LEFT, padx=10)

        right_button = Button(center_frame, text='>', command=self.show_next_date, bg='#1a2530', fg='white', border=0,
                              width=2, height=1, font=('Helvetica', 12))
        right_button.pack(side=tk.RIGHT, padx=10)

        self.show_current_date()

        self.take_attendance_button = Button(self, text='Take Attendance', command=self.show_take_attendance_window,
                                              bg='#1a2530', fg='white', border=0, width=20, height=1, font=('Helvetica', 12))
        self.take_attendance_button.pack(pady=20)

        # Add random data for the old dates
        for date in self.dates:
            self.attendance_data[date] = {f'Student {i}': random.choice(['Present', 'Absent', 'Leave']) for i in range(1, 6)}
        
        self.update_attendance_table(self.dates[self.current_date_index])

    def show_previous_date(self):
        if self.current_date_index > 0:
            self.current_date_index -= 1
            self.show_current_date()

    def show_next_date(self):
        if self.current_date_index < len(self.dates) - 1:
            self.current_date_index += 1
            self.show_current_date()

    def show_current_date(self):
        current_date = self.dates[self.current_date_index]
        self.date_var.set(f'Date: {current_date}')
        self.update_attendance_table(current_date)

    def update_attendance_table(self, date):
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)

        if date not in self.attendance_data:
            self.attendance_data[date] = {}

        student_data = self.attendance_data[date].items()
        for student, status in student_data:
            self.attendance_tree.insert('', 'end', values=(student, status))

    def show_take_attendance_window(self):
        take_attendance_window = TakeAttendanceWindow(self)

    def save_attendance(self, date, attendance_data):
        self.attendance_data[date] = {student: status for student, status in attendance_data}
        self.dates.append(date)  # Add the new date to the list
        self.current_date_index = len(self.dates) - 1  # Set the index to the new date
        self.show_current_date()


class TakeAttendanceWindow(tk.Toplevel):
    def __init__(self, admin_attendance):
        super().__init__(admin_attendance.master)
        self.title('Take Attendance')
        self.admin_attendance = admin_attendance
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text='Enter Date:', font=('Helvetica', 12)).pack()
        self.date_entry = Entry(self)
        self.date_entry.pack(pady=10)

        save_button = Button(self, text='Save', command=self.show_attendance_editor_and_close, bg='#1a2530', fg='white', border=0,
                             font=('Helvetica', 12))
        save_button.pack(pady=20)

    def show_attendance_editor_and_close(self):
        date = self.date_entry.get()
        attendance_data = [(f'Student {i}', '') for i in range(1, 6)]  # Empty data for now
        editor_window = AttendanceEditorWindow(self, date, attendance_data)

class AttendanceEditorWindow(tk.Toplevel):
    def __init__(self, take_attendance_window, date, attendance_data):
        super().__init__(take_attendance_window)
        self.title('Attendance Editor')
        self.take_attendance_window = take_attendance_window
        self.date = date
        self.attendance_data = attendance_data
        self.student_vars = []  # Store student and status variables

        self.create_widgets()

    def create_widgets(self):
        # Create a frame to hold the student attendance widgets and scrollbar
        frame = tk.Frame(self)
        frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to hold the frame and attach the scrollbar
        canvas = tk.Canvas(frame)
        canvas.pack(side=LEFT, fill=tk.BOTH, expand=True)

        # Attach scrollbar to the canvas
        scrollbar = Scrollbar(frame, command=canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create another frame to hold the student attendance widgets
        inner_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor='nw')

        # Create student attendance widgets
        for student, status in self.attendance_data:
            student_frame = tk.Frame(inner_frame)
            student_frame.pack(side=tk.TOP, pady=5)

            student_var = StringVar(value=student)
            tk.Label(student_frame, textvariable=student_var, width=20, anchor='w').pack(side=LEFT)
            status_var = StringVar(value=status)
            Radiobutton(student_frame, text='Absent', variable=status_var, value='Absent').pack(side=LEFT)
            Radiobutton(student_frame, text='Present', variable=status_var, value='Present').pack(side=LEFT)
            Radiobutton(student_frame, text='Leave', variable=status_var, value='Leave').pack(side=LEFT)

            # Store student and status variables
            self.student_vars.append((student_var, status_var))

        # Add the Save button
        save_button = Button(inner_frame, text='Save', command=self.save_attendance, bg='#1a2530', fg='white', border=0,
                             font=('Helvetica', 12))
        save_button.pack(pady=20)

        # Update the scroll region of the canvas
        inner_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

    def save_attendance(self):
        # Get the updated attendance data
        updated_attendance_data = [(student_var.get(), status_var.get()) for student_var, status_var in self.student_vars]
        
        # Save the attendance data and update the Treeview
        self.take_attendance_window.admin_attendance.save_attendance(self.date, updated_attendance_data)
        self.take_attendance_window.destroy()  # Close the TakeAttendanceWindow
        self.destroy()  # Close the AttendanceEditorWindow
