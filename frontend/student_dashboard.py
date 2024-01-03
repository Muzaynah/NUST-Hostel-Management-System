import tkinter as tk
from tkinter import Label, Button, PhotoImage, Listbox, Scrollbar, messagebox
import mysql.connector
from config import db_config_student
import config

class StudentDashboard(tk.Frame):
    def __init__(self, master, show_outpass, show_complaints, show_attendance):
        super().__init__(master, bg='white')
        self.master = master
        self.show_outpass = show_outpass
        self.show_complaints = show_complaints
        self.show_attendance = show_attendance
        self.connection = mysql.connector.connect(**db_config_student)
        self.cursor = self.connection.cursor()
        self.view_name = str(config.current_user_id[0]) + '_student'

        self.create_widgets()

    def show_notification_detail(self, event):
        selected_index = notification_listbox.curselection()
        if selected_index:
            selected_text = notification_listbox.get(selected_index)
            messagebox.showinfo("Notification Detail", selected_text)

    def create_widgets(self):
        # Top panel displaying the student's name
        top_panel = tk.Frame(self, bg='#014a81')  # Use a light blue color
        top_panel.pack(side=tk.TOP, fill=tk.X)

        # Load a sample profile picture (replace with the actual path to the image file)
        original_image = PhotoImage(file='assets/NUSTlogo.png')

        # Define the size for the profile picture
        desired_width = 100
        desired_height = 100

        # Resize the image using the subsample method
        resized_image = original_image.subsample(
            int(original_image.width() / desired_width),
            int(original_image.height() / desired_height)
        )

        # Create a label for the profile picture
        profile_label = Label(top_panel, image=resized_image, bg='#014a81')
        profile_label.image = resized_image
        profile_label.pack(side=tk.LEFT, padx=50, pady=50)

        # get the actual students data from db
        out_params = [None] * 18
        result = self.cursor.callproc('get_all_student_data', [config.current_user_id[0]] + out_params)
        id, firstName, lastName, age, email, phoneNumber, city, street, house_no, full_address, roomNumber, batch, username, password, program, hostel_id, department_id, hostel_name, department_name = result
        self.hostel_id = hostel_id

        student_name_label = Label(top_panel, text=f"{firstName + ' ' + lastName}\nCMS: {config.current_user_id[0]}",
                                   font=('Microsoft YaHei UI Light', 20, 'bold'), bg='#014a81', fg='white', anchor=tk.W, justify=tk.LEFT)
        student_name_label.pack(side=tk.LEFT, padx=100, pady=10)

        # Create a label for more of the student's information
        student_info_label = Label(top_panel, text=f"{department_name}\t\t{hostel_name} Hostel\n{program}\t\t#{roomNumber}",
                                   font=('Microsoft YaHei UI Light', 20), bg='#014a81', fg='white', anchor=tk.E, justify=tk.LEFT)
        student_info_label.pack(side=tk.RIGHT, padx=100, pady=10)

        # Left panel for buttons
        left_panel = tk.Frame(self, bg='white')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(350, 0), pady=(180, 0))

        # Buttons for different sections
        button_bg_color = '#1a2530'  # Light blue color for buttons

        Button(left_panel, text='Outpass', command=self.show_outpass, bg=button_bg_color, fg='#3a80b5', border=0, width=20, height=1,
               font=('Microsoft YaHei UI Light', 18)).pack(pady=(0, 6), anchor=tk.NW)
        Button(left_panel, text='Complaints', command=self.show_complaints, bg=button_bg_color, fg='#3a80b5', border=0, width=20,
               height=1, font=('Microsoft YaHei UI Light', 18)).pack(pady=6, anchor=tk.NW)
        Button(left_panel, text='Attendance', command=self.show_attendance, bg=button_bg_color, fg='#3a80b5', border=0, width=20,
               height=1, font=('Microsoft YaHei UI Light', 18)).pack(pady=6, anchor=tk.NW)

        # Right panel for notifications
        right_panel = tk.Frame(self, bg='#1a2530', width=250, height=300)
        right_panel.pack(side=tk.RIGHT, anchor=tk.N, padx=(0, 60), pady=60)

        # Label for Notifications
        notification_label = Label(right_panel, text='Notifications', font=('Microsoft YaHei UI Light', 16), bg='#1a2530',
                                   fg='white')
        notification_label.pack(side=tk.TOP, pady=(10, 10))

        # Listbox for notifications
        global notification_listbox
        notification_listbox = Listbox(right_panel, bg='#d6d9dc', fg='black', selectbackground='#1f2b38',
                                       selectforeground='white', font=('Microsoft YaHei UI Light', 12), width=25, height=100)
        notification_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the listbox
        global scrollbar
        scrollbar = Scrollbar(right_panel, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the listbox to work with the scrollbar
        notification_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=notification_listbox.yview)

        # # Sample notifications (replace with your actual notifications)
        # notifications = ["Tomorrow's breakfast timing: From 0900hrs to 1030hrs",
        #                   "Dear students, Please be advised that hostelites are prohibited from inviting any guests, "
        #                   "siblings, or friends inside the hostel premises. Any individual found bringing a candidate "
        #                   "for the NUST Entry Test (NET) into the hostel will face strict disciplinary action. "
        #                   "Additionally, the NET of the said candidate will be cancelled.",
        #                   "Notification 3", "Notification 4", "Notification 5", "Notification 6",
        #                   "Notification 7", "Notification 8", "Notification 9", "Notification 10", "Notification 11",
        #                   "Notification 12", "Notification 13", "Notification 14", "Notification 15", "Notification 16",
        #                   "Notification 17", "Notification 18", "Notification 19", "Notification 20",
        #                   "Notification 21", "Notification 22", "Notification 23", "Notification 24", "Notification 25",
        #                   "Notification 26", "Notification 27", "Notification 28", "Notification 29", "Notification 30"]

        query = f"SELECT NText FROM Notifications WHERE HID = {self.hostel_id}"
        self.cursor.execute(query)
        notifications = self.cursor.fetchall()
        # Insert notifications into the listbox
        [notification_listbox.insert(tk.END, notification[0]) for notification in notifications]

        # Bind a callback to handle notification selection
        notification_listbox.bind('<<ListboxSelect>>', self.show_notification_detail)
