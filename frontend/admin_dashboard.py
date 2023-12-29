import tkinter as tk
from tkinter import Label, Button, PhotoImage, Listbox, Scrollbar, messagebox
import mysql.connector
from config import db_config
import config

#1f2b38 dark
#E0E6EE bg light
#014a81 nust blue
#2270ab lighter nust blue

class AdminDashboard(tk.Frame):
    def __init__(self, master, show_moutpass, show_mcomplaint, show_mattendance, show_mstudent, show_mnotification):
        super().__init__(master, bg='white')  # Set background color to white
        self.master = master
        self.show_moutpass = show_moutpass
        self.show_mcomplaint = show_mcomplaint
        self.show_mattendance = show_mattendance
        self.show_mstudent = show_mstudent
        self.show_mnotification = show_mnotification
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()

        self.create_widgets()

    def create_widgets(self):
        # Top panel displaying the admin's info
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
        profile_label.image = resized_image  # Keep a reference to the resized image
        profile_label.pack(side=tk.LEFT, padx=50, pady=50)

        # get the actual admin's data from db
        query = f"SELECT CONCAT(mFirstName, ' ',mLastName) FROM Manager WHERE MID = '{config.current_user_id[0]}'"
        self.cursor.execute(query)
        admin_name = self.cursor.fetchone()
        
        admin_id = config.current_user_id

        query = f"SELECT hName FROM Hostel, Manager WHERE Manager.HID = Hostel.HID and MID = '{config.current_user_id[0]}'"
        self.cursor.execute(query)
        Hostel = self.cursor.fetchone()
    
       #  admin_name = "Samina Baji"
       #  admin_id = '1234'
       #  Hostel = 'Amna Hostel'
       #  Role = 'Caretaker'

        # label for the admin's name and id
        admin_name_label = Label(top_panel, text=f"Name: {admin_name[0]}\nID: {admin_id[0]}",
                                   font=('Microsoft YaHei UI Light', 20, 'bold'), bg='#014a81', fg='white', anchor=tk.W, justify=tk.LEFT)
        admin_name_label.pack(side=tk.LEFT, padx=100, pady=10)

        # label for more of the admin's information
        admin_info_label = Label(top_panel, text=f"Hostel Name: {Hostel[0]}\n",
                                   font=('Microsoft YaHei UI Light', 20), bg='#014a81', fg='white', anchor=tk.W, justify=tk.LEFT)
        admin_info_label.pack(side=tk.RIGHT, padx=150, pady=10)

        # central panel for buttons
        main_panel = tk.Frame(self, bg='white')
        main_panel.pack(side=tk.TOP, fill=tk.Y, padx=30, pady=(60,0))

        # Buttons for different sections
        # manage attendance 
        # manage complaints 
        # manage outpasses
        # manage students
        # manage hostels
        # manage notifications

        button_bg_color = '#1a2530'  # dark color for buttons
        Button(main_panel, text='Manage Attendance', pady = 10, command=self.show_mattendance, bg=button_bg_color, fg='#3a80b5', border=0, width=25, height=1,
               font=('Microsoft YaHei UI Light', 18)).pack(pady=(0, 10))
        Button(main_panel, text='Manage Complaints', pady = 10, command=self.show_mcomplaint, bg=button_bg_color, fg='#3a80b5', border=0, width=25, height=1,
               font=('Microsoft YaHei UI Light', 18)).pack(pady=(0, 10))
        Button(main_panel, text='Manage Outpasses', pady = 10, command=self.show_moutpass, bg=button_bg_color, fg='#3a80b5', border=0, width=25, height=1,
               font=('Microsoft YaHei UI Light', 18)).pack(pady=(0, 10))
        Button(main_panel, text='Manage Students', pady = 10, command=self.show_mstudent, bg=button_bg_color, fg='#3a80b5', border=0, width=25, height=1,
               font=('Microsoft YaHei UI Light', 18)).pack(pady=(0, 10))
        Button(main_panel, text='Manage Notifications', pady = 10, command=self.show_mnotification, bg=button_bg_color, fg='#3a80b5', border=0, width=25, height=1,
               font=('Microsoft YaHei UI Light', 18)).pack(pady=(0, 10))