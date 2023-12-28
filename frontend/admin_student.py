import tkinter as tk
from tkinter import Label, Button, PhotoImage, ttk, Entry, Toplevel

class AdminStudent(tk.Frame):
    def __init__(self, master, show_add_student):
        super().__init__(master, bg='white')
        self.master = master
        self.show_add_student = show_add_student
        self.create_widgets()

    def create_widgets(self):

        # Create a frame to center the treeview
        center_frame = tk.Frame(self, bg='white')
        center_frame.pack(expand=True, fill='both')
        
        # Create a treeview for displaying students
        columns = ('CMS', 'First Name', 'Last Name', 'Age', 'Email', 'Phone Number', 'City', 'Street', 'House Number', 'Batch', 'Hostel', 'Room Number', 'Department', 'Program')
        self.student_tree = ttk.Treeview(center_frame, columns=columns, show='headings', selectmode='browse')

        # Set column headings
        for col in columns:
            self.student_tree.heading(col, text=col)

        # Set column widths
        for col in columns:
            self.student_tree.column(col, width=100)

        self.student_tree.pack(padx=20, pady=40, side=tk.TOP, fill=tk.BOTH, expand=True)

        # Add a scrollbar to the treeview
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.student_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.student_tree.configure(yscrollcommand=scrollbar.set)

        add_student_button = Button(self, text='Add Student', command=self.master.show_add_student, bg='#1a2530', fg='white', border=0, width=20, height=1,
                            font=('Microsoft YaHei UI Light', 14))

        add_student_button.pack(pady=40)

    def update_student_table(self, student_data):
        # Clear existing items in the treeview
        for item in self.student_tree.get_children():
            self.student_tree.delete(item)

        # Insert new student data into the treeview
        for student in student_data:
            self.student_tree.insert('', 'end', values=student)

class AddStudentWindow(tk.Toplevel):
    def __init__(self, master, add_student_callback):
        super().__init__(master)
        self.title('Add Student')

        # Set the size of the window
        self.width = 450
        self.height = 650

        # Calculate the position to center the window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2

        # Set the geometry of the window
        self.geometry(f'{self.width}x{self.height}+{x}+{y}')

        self.add_student_callback = add_student_callback
        self.create_widgets()

    def create_widgets(self):
        # Create entry fields for student information
        labels = ['CMS', 'First Name', 'Last Name', 'Age', 'Email', 'Phone Number', 'City', 'Street', 'House Number',
                  'Batch', 'Hostel', 'Room Number', 'Department', 'Program']
        self.entry_fields = {}

        for label in labels:
            tk.Label(self, text=label).pack()
            entry = Entry(self)
            entry.pack()
            self.entry_fields[label] = entry

        # Add a button to save the student
        save_button = Button(self, text='Save', command=self.save_student, bg='#1a2530', fg='white', border=0,
                             font=('Microsoft YaHei UI Light', 12))
        save_button.pack(pady=20)

    def save_student(self):
        # Retrieve data from entry fields and call the callback to add the student
        student_data = {label: entry.get() for label, entry in self.entry_fields.items()}
        self.add_student_callback(student_data)
        self.destroy()