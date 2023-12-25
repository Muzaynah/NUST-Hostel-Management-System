import tkinter as tk
from tkinter import Label, Button, PhotoImage, Listbox, Scrollbar, messagebox

#1f2b38 dark
#E0E6EE bg light
#014a81 nust blue
#2270ab lighter nust blue


class StudentDashboard(tk.Frame):
    def __init__(self, master, show_outpass, show_complaints, show_attendance):
        super().__init__(master, bg='white')  # Set background color to white
        self.master = master
        self.show_outpass = show_outpass
        self.show_complaints = show_complaints
        self.show_attendance = show_attendance
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
        profile_label.image = resized_image  # Keep a reference to the resized image
        profile_label.pack(side=tk.LEFT, padx=50, pady=50)

        # get the actual students data from db
        student_name = "Misra Fatima"  # Replace this with the actual student's name
        CMS_id = '123456'
        Department = 'SEECS'
        Program = 'Computer Science'
        Hostel = 'Amna Hostel'
        RoomNumber = '#316'

        # Create a label for the student's name and cms
        student_name_label = Label(top_panel, text=f"{student_name}\n\n{CMS_id}",
                                   font=('Helvetica', 14), bg='#014a81', fg='white', anchor=tk.W, justify=tk.LEFT)
        student_name_label.pack(side=tk.LEFT, padx=100, pady=10)

        # Create a label for more of the student's information
        student_info_label = Label(top_panel, text=f"{Department}\t\t\t{Program}\n\n{Hostel}\t\t{RoomNumber}",
                                   font=('Helvetica', 14), bg='#014a81', fg='white', anchor=tk.E, justify=tk.LEFT)
        student_info_label.pack(side=tk.RIGHT, padx=100, pady=10)

        # Left panel for buttons
        left_panel = tk.Frame(self, bg='white')
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(350,0), pady=(180,0))

        # Buttons for different sections
        button_bg_color = '#1a2530'  # Light blue color for buttons

        # Adjusting the size and position of buttons
        Button(left_panel, text='Outpass', command=self.show_outpass, bg=button_bg_color, fg='white', border=0, width=30, height=2,
               font=('Helvetica', 14)).pack(pady=(0, 10), anchor=tk.NW)  # Use anchor=tk.NW to align to the top-left corner)
        Button(left_panel, text='Complaints', command=self.show_complaints, bg=button_bg_color, fg='white',border=0, width=30,
               height=2, font=('Helvetica', 14)).pack(pady=10, anchor=tk.NW)  # Use anchor=tk.NW to align to the top-left corner)
        Button(left_panel, text='Attendance', command=self.show_attendance, bg=button_bg_color, fg='white',border=0, width=30,
               height=2, font=('Helvetica', 14)).pack(pady=10, anchor=tk.NW)  # Use anchor=tk.NW to align to the top-left corner)
        

        # Right panel for notifications
        right_panel = tk.Frame(self, bg='#1a2530', width=250, height=300)
        right_panel.pack(side=tk.RIGHT, anchor=tk.N, padx=(0,60), pady=60)

        # Label for Notifications
        notification_label = Label(right_panel, text='Notifications', font=('Helvetica', 16), bg='#1a2530', fg='white')
        notification_label.pack(side=tk.TOP, pady=(10, 10))

        # Listbox for notifications
        global notification_listbox  # Make the listbox global to access it in the callback function
        notification_listbox = Listbox(right_panel, bg='#d6d9dc', fg='black', selectbackground='#1f2b38',
                               selectforeground='white', font=('Helvetica', 12), width=25, height=100)
        notification_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the listbox
        global scrollbar  # Make the scrollbar global
        scrollbar = Scrollbar(right_panel, orient=tk.VERTICAL)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the listbox to work with the scrollbar
        notification_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=notification_listbox.yview)

        # Sample notifications (replace with your actual notifications)
        notifications = ["Tomorrow's breakfast timing: From 0900hrs to 1030hrs",
                          "Dear students, Please be advised that hostelites are prohibited from inviting any guests, "
                          "siblings, or friends inside the hostel premises. Any individual found bringing a candidate "
                          "for the NUST Entry Test (NET) into the hostel will face strict disciplinary action. "
                          "Additionally, the NET of the said candidate will be cancelled.",
                          "Notification 3", "Notification 4", "Notification 5", "Notification 6",
                          "Notification 7", "Notification 8", "Notification 9", "Notification 10", "Notification 11",
                          "Notification 12", "Notification 13", "Notification 14", "Notification 15", "Notification 16",
                          "Notification 17", "Notification 18", "Notification 19", "Notification 20",
                          "Notification 21", "Notification 22", "Notification 23", "Notification 24", "Notification 25", 
                          "Notification 26", "Notification 27", "Notification 28", "Notification 29", "Notification 30"]

        # Insert notifications into the listbox
        [notification_listbox.insert(tk.END, notification) for notification in notifications]

        # Bind a callback to handle notification selection
        notification_listbox.bind('<<ListboxSelect>>', self.show_notification_detail)

# Main application
if __name__ == "__main__":
    app = tk.Tk()
    app.title('NUST Hostel Management System')
    app.geometry('1200x600+50+20')
    app.iconbitmap('assets/nust_logo.ico')

    student_dashboard = StudentDashboard(app, None, None, None)
    student_dashboard.pack(fill=tk.BOTH, expand=True)

    app.mainloop()
